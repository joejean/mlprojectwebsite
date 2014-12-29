from scikits.crab.models import MatrixPreferenceDataModel
from scikits.crab.metrics import euclidean_distances
from scikits.crab.similarities import UserSimilarity, ItemSimilarity
from scikits.crab.recommenders.knn import UserBasedRecommender, ItemBasedRecommender
from scikits.crab.recommenders.knn.item_strategies import ItemsNeighborhoodStrategy
from scikits.crab.metrics.classes import CfEvaluator



#Custom functions that return recommendations, 10 by default
def custom_recommend(dataset, recommend_to, num_of_recommendations = 10):
	#This is based on the USER-BASED RECOMMENDATION Model
	#Build the model. It returns a dictionary of the recommendations
	model = MatrixPreferenceDataModel(dataset)

	similarity = UserSimilarity(model, euclidean_distances)

	#Build the Recommender
	recommender = UserBasedRecommender(model, similarity, with_preference = True)

	return recommender.recommend(recommend_to, num_of_recommendations)
