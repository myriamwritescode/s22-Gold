import numpy as NP
import math

user_score = [12, 7, 21, 8, 19, 4, 0, 10]
rep_score = [10, 10, 11, 9, 5, 20, 14, 0]

# subtract user_score from rep_score
service_vector = NP.subtract(user_score, rep_score)

#find magnitude of the resulting vector
service_magnitude = math.sqrt(sum(pow(element, 2) for element in
                                  service_vector))



