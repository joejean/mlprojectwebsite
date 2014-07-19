from scikits.crab.models import MatrixPreferenceDataModel
from scikits.crab.metrics import euclidean_distances
from scikits.crab.similarities import UserSimilarity, ItemSimilarity
from scikits.crab.recommenders.knn import UserBasedRecommender, ItemBasedRecommender
from scikits.crab.recommenders.knn.item_strategies import ItemsNeighborhoodStrategy
from scikits.crab.metrics.classes import CfEvaluator

###Categories
#Men's Clothing: 1
#Women's Clothing: 2
#Men's Footwear: 3
#Women's Footwear: 4
#Restaurant: 5
#Consumer Electronics: 6
#Jewelry: 7
#Children's Clothing: 8
#Beauty Products: 9
#Telecommunication: 10

#Given a mall with its stores, would the store x be a good fit?

dataset = {	'FirstMall': {'Men\'s Clothing':8, 'Beauty Products':11, 'Consumer Electronics':11},
			'SecondMall': {'Men\'s Clothing':3, 'Women\'s Footwear':12, 'Jewelry': 3},
			'ThirdMall': {'Telecommunication':9,'Children\'s Clothing':4},
			'Fourthmall':{'Restaurant':12,"Men's Footwear":4, 'Beauty Products':13 },
			'FithMall': {'Consumer Electronics':13, 'Restaurant': 1, 'Men\'s Clothing':14 },
			'SixthMall' : {'Jewelry':15, 'Telecommunication':14, 'Men\'s Footwear':4 },
			'SeventhMall':{'Women\'s Footwear':5,'Consumer Electronics':2, 'Jewelry':12, 'Restaurant':14 },
			'EigthMall':{'Beauty Products': 11, 'Men\'s Clothing':8}
			
		  }


# #Recommender for Mall 3
# print "UserBased:" 
# print recommender.recommend('EigthMall')
# print 'Userbased Evaluation Score'
# print all_scores

def custom_recommender(dataset, recommend_to):
	#This is based on the USER-BASED RECOMMENDATION Model
	#Build the model. It returns a dictionary of the recommendations
	model = MatrixPreferenceDataModel(dataset)

	similarity = UserSimilarity(model, euclidean_distances)

	#Build the Recommender
	recommender = UserBasedRecommender(model, similarity, with_preference = True)

	#Evaluate the module. This does not necessarily work in production.
	evaluator = CfEvaluator()
	all_scores = evaluator.evaluate(recommender, permutation=False)

	return recommender.recommend(recommend_to)


# #ITEM-Based Recommendation - Not Quite Good!
# model = MatrixPreferenceDataModel(dataset)
# items_strategy = ItemsNeighborhoodStrategy()
# similarity = ItemSimilarity(model, euclidean_distances)

# recommender = ItemBasedRecommender(model, similarity, items_strategy)

# #instantiate Evaluator
# evaluator = CfEvaluator()
# all_scores = evaluator.evaluate(recommender, permutation=False)

# print "ItemBased:" 
# print recommender.recommend('EigthMall')
# print 'ItemBased Evaluation Score'
# print all_scores
