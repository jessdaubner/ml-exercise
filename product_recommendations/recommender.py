"""Builds a collaborative filtering model using Spark ML's ALS-WR implementation
   to provide the top 10 product recommendations for customers and products with
   prior purchase history.
"""
import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import isnull, col, explode

from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder

from config import logger, RAW_DATA, RECS


def preprocess(df):
    """Drops null values in customer_id and global_product_id and
       calculates purchase count of each product by customer.
    Args:
       df (DataFrame): raw data from CSV file
    Returns:
       DataFrame with columns customer_id, global_product_id, count
    """
    logger.info('Raw data contains {:,} rows'.format(df.count()))
    df = (df.select(col('customer_id').cast('integer'),
                    col('global_product_id').cast('integer'))
          .filter(~isnull('customer_id') & ~isnull('global_product_id')))
    df.cache()
    logger.info('Cleaned data contains {:,} rows'.format(df.count()))

    df = df.groupBy('customer_id', 'global_product_id').count()
    logger.info('Customer product purchases contains {:,} rows'.format(df.count()))
    logger.info('Customer product purchases contains {:,} customers'
                .format(df.select('customer_id').distinct().count()))
    logger.info('Customer product purchases contains {:,} products'
                .format(df.select('global_product_id').distinct().count()))
    logger.info('Customer total product purchases summary statistics:')
    df.select('count').describe().show()
    return df


def run_cross_validation(als, train):
    """Fits ALS model use K-folds cross validation
    Args:
      als (pyspark.ml.recommendation.ALS): ALS model instance
      train (DataFrame): training dataset
    Returns:
      best fitted ALS model
    """
    logger.info('Training ALS model with k-fold cross-validation..........')

    param_grid = (ParamGridBuilder()
                  .addGrid(als.rank, [5, 10])
                  .addGrid(als.maxIter, [10, 25, 50])
                  .addGrid(als.regParam, [0.1, 0.01])
                  .build())

    cv = CrossValidator(estimator=als,
                        estimatorParamMaps=param_grid,
                        evaluator=RegressionEvaluator(labelCol='count'),
                        numFolds=5,
                        parallelism=10,
                        seed=42)

    # NOTE: Cut dataframe lineage before cross-validation to avoid local StackOverflow error
    spark.sparkContext.setCheckpointDir("/tmp")

    cv_model = cv.fit(train)
    best_model = cv_model.bestModel
    logger.info('Average cross-validation RMSE by submodel: {}'.format(cv_model.avgMetrics))
    logger.info('Lowest cross-validation submodel RMSE: {}'.format(round(min(cv_model.avgMetrics), 3)))
    return best_model


def train_evaluate(df, cross_validate):
    """Creates train and test sets, builds an ALS-WR model using cross-validation,
       and evaluates the model on a test set.
    Args:
      df (DataFrame): DataFrame of user-item interactions
      cross_validate (boolean): Run cross-validation or not
    Returns:
      ALS model
    """
    train, test = df.randomSplit([0.8, 0.2], seed=42)
    logger.info('Training set contains {:,} examples'.format(train.count()))
    logger.info('Test set contains {:,} examples'.format(test.count()))
    als = ALS(implicitPrefs=True,
              userCol='customer_id',
              itemCol='global_product_id',
              ratingCol='count',
              coldStartStrategy='drop')
    if cross_validate:
        model = run_cross_validation(als, train)
    else:
        als.setParams(rank=10,
                      maxIter=10,
                      regParam=0.1)
        model = als.fit(train)
    evaluator = RegressionEvaluator(metricName='rmse',
                                    labelCol='count',
                                    predictionCol='prediction')
    for name, dataset in {'Train': train, 'Test': test}.items():
        predictions = model.transform(dataset)
        rmse = evaluator.evaluate(predictions)
        logger.info(f'{name} RMSE: {rmse:.4f}')
    return model


def make_recommendations(model, n_recs=10):
    """Recommends top 10 products for all users and writes them to CSV file
    Args:
      model (spark.ml.recommendation.ALS): trained ALS model
      n_recs (int): number of product recommendations to make for each customer
    Returns:
      DataFrame with columns customer_id, global_product_id, rating
    """
    recs = model.recommendForAllUsers(n_recs)
    formatted_recs = (recs
                      .select('customer_id', explode(col('recommendations')))
                      .select('customer_id',
                              col('col').getItem('global_product_id').alias('global_product_id'),
                              col('col').getItem('rating').alias('rating')))
    logger.info('Total Product Recommendations: {:,}'.format(formatted_recs.count()))
    logger.info('Writing top {n_recs} product recommendations for all customers to {RECS}'
                .format(n_recs=n_recs, RECS=RECS))
    formatted_recs.write.csv(RECS)
    return formatted_recs


def get_recs_by_customer_id(recs, customer_id):
    """Returns recommended global product ids for customer_id provided
    Args:
      recs (DataFrame): DataFrame with columns customer_id, global_product_id, rating
      customer_id (int): customer_id
    Returns:
    """
    customer_specific_recs = (recs
                              .filter(col('customer_id') == customer_id)
                              .drop('customer_id')
                              .collect())
    product_recs = [row['global_product_id'] for row in customer_specific_recs]
    logger.info('Top product recommendations for customer_id {}: {}'
                .format(customer_id, product_recs))
    return product_recs


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cross-validate', action='store_true',
                        help='Run cross-validation or use previously discovered hyper-parameters NOTE: This takes a while!')
    parser.add_argument('--customer_id', default=None,
                        help='Specific customer_id to retreive product recommendations')

    args = parser.parse_args()
    logger.debug(f'Passed arguments: cross-validate={args.cross_validate}, customer_id={args.customer_id}')

    spark = (SparkSession.builder
             .appName('Product Recommendations')
             .getOrCreate())
    spark.sparkContext.setLogLevel("ERROR")

    data = spark.read.csv(RAW_DATA, header=True)
    user_item_interactions = preprocess(data)
    model = train_evaluate(user_item_interactions, args.cross_validate)
    all_recs = make_recommendations(model)
    get_recs_by_customer_id(all_recs, customer_id=args.customer_id)
