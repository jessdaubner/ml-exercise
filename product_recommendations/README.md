# Product Recommendations
Builds a collaborative filtering model using Spark ML's ALS-WR implementation to provide the top 10 product recommendations for customers and products with prior purchase history.

## Setup & Running Recommender
Build and run app with Docker:
```
cd ml-exercise
docker build -t recommender product_recommendations/
docker run --rm -ti recommender
```

## Methodology
The code in `recommender.py` develops a collaborative filtering model using Spark ML's ALS estimator to recommend the 10 most relevant products to each user. The raw data is preprocessed so that transactions without `global_product_id` or `customer_id` are discarded and transaction data is grouped by `global_product_id` for each customer and counted. The total purchase counts are then used as a measure of the customer's preference or rating for a given product. An 80%/20% train-test split is used and an ALS model is then selected using k-folds cross-validation (k=5).
### Results
Expected results from running the application:
```
INFO | Raw data contains 1,215,193 rows
INFO | Cleaned data contains 902,792 rows
INFO | Customer product purchases contains 595,226 rows
INFO | Customer product purchases contains 6,982 customers
INFO | Customer product purchases contains 90,542 products
INFO | Customer total product purchases summary statistics:
+-------+------------------+
|summary|             count|
+-------+------------------+
|  count|            595226|
|   mean|1.5167213797784371|
| stddev|  1.52147607562779|
|    min|                 1|
|    max|               139|
+-------+------------------+

INFO | Training set contains 476,043 examples
INFO | Test set contains 119,183 examples
INFO | Train RMSE: 2.0799
INFO | Test RMSE: 2.1196
INFO | Total Product Recommendations: 69,640
INFO | Writing top 10 product recommendations for all customers to recommender/data/recommendations.csv
INFO | Top product recommendations for customer_id 14687389: [934387, 156309, 156322, 156329, 155230, 148407, 148695, 148680, 152459, 148789]
```

### Customer Example
Examining the product recommendations for `customer_id` 14687389 reveals that the customer's most frequently purchased `global_product_id`, 934387, is the top recommendation. Unfortunatetly, this product ID is reused across different items making it somewhat of a catch-all generic product and that recommendation not particuarly useful. Overall, the mean average precision for the user's recommendations was 0.59. Of the recommendations, four `global_product_ids` had not been purchased previously (148680, 152459, 148789, 148407). All of these new products are in previously purchased categories (e.g. fruits and vegetables) and two are new items overall (e.g. avocado and cucumber).

#### Offline and Online Metrics
Given more time, I would calculate more common ranking metrics used to evaluate ordered recommendation predictions offline such as mean average precision (MAP), nDCG, and precision at k. Additionally, it would be insightful to understand the recommender's coverage, diversity, and novelty. For online metrics, the click-through rate or time on page of specific products in campaigns or overall would be a better metric to use since purchases will occur less frequently and these metrics can still provide information on overall user engagement with recommendations or the app overall.

### New Users
This solution would not provide recommendations to new users since customers and products must have historical purchase data to be included in the user-item interaction matrix. Initially, new users could receive recommendations based on popular or trending products within their geographic or demographic. To improve recommendations for new users, additional implicit feedback such as product offers viewed or saved or the CTR of specific product ads within the app could be used instead of purchase transactions alone.

#### Other Metrics
Other than user relevancy, relevant business metrics for a given product such as profit (maybe indirectly through CPM or CPC for given product campaigns) could be used to weight recommendations. For example, TensorFlow's [WALS estimator](https://www.tensorflow.org/api_docs/python/tf/contrib/factorization/WALSMatrixFactorization) can be initialized with row and column weights so that products with higher profit margins would be recommended more frequently.

## Deployment
### Batch
Batch product remmendations could be made by running the Spark application periodically, perhaps daily, on EMR to update and write recommendations to a NoSQL database table as new transaction data becomes available. The table can then be queried by another service, for example by using `customer_id` as the primary key, to provide personalized recommendations to users of the app. The Spark cluster size can be scaled horizontally as needed to compute recommendations for more than 25 million users and a NoSQL database such as DynamoDB has no item limits and read and write capacity can scale on-demand.
### Real-Time
If the existing architecture already includes streaming data via Kinesis or Kafka, a Spark Streaming application could be used to apply the model trained offline to streaming data to make recommendations in real-time. Spark's MLlib does not support a Streaming ALS estimator (like [`StreamingKmeans`](https://spark.apache.org/docs/latest/mllib-clustering.html#streaming-k-means)), so the model would not simultaneously learn from incoming data and the predictions would effectively be the same as the batch training approach. Unfortunately, this model could not easily be integrated with AWS SageMaker to take advantage of its endpoints for real-time inference because the `sagemaker_pyspark` library does not offer an estimator to extend Spark's ALS implementation (see `sagemaker_pyspark` [algorithms](https://github.com/aws/sagemaker-spark/tree/master/sagemaker-pyspark-sdk/src/sagemaker_pyspark/algorithms). Additionally, [Spark does not support exporting ALS estimators to PMML](https://spark.apache.org/docs/latest/mllib-pmml-model-export.html#sparkmllib-supported-models), which could also be used with [AWS Lambda to serve predictions in real-time](https://aws.amazon.com/blogs/machine-learning/build-pmml-based-applications-and-generate-predictions-in-aws/).

## Next Steps
* Experiment with scaling product purchases or mapping them to another scale and removing the most popular items during preprocessing (since a user is likely to select these by default)
* Exploring other ALS implementations, such as TensorFlow's WALS implementation, and other models like factorization machines that can incorporate user and product information would likely lead to better performance
* Develop a hybrid recommender that incorporates predictions from content-based and collaborative filtering models; such a system would be more robust overall and could also handle new users better, especially if users answered initial survey questions about about stores, brands, or products they liked
