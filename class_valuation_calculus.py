"""
Primary Class for Option Valuation, calculates binomial, BlackSholes and Put Call Parity
"""
import numpy as np


class valuation_calculus():

    def __init__(self):
        #self.data_valuationNeed = {}
        self.data_valuationNeed = {"option_type": 3, "option_spot": 3200,
                                   "option_strike": 3250, "option_rate": 0.0425,
                                   "option_sd_risk": 0.17, "option_time_years": 90,
                                   "option_delta_time": 0.01666666666666670, "option_nodes_calc": 15}

    # Data Need for Valuation
    # tipo de opción call o put
    # americana o europea
    # spot
    # strike
    # tasa de interés Continua
    # volatilidad
    # plazo en días
    # Base
    # Número de nodos deseado
    # Calculo de delta de T se cálcula
    def construct_info_need_valuate(self):
        print("Tipo de Opción ")
        print("")
        print("1.Call Europea")
        print("2.Put Europea")
        print("3.Call Americana")
        print("4.Put Americana")
        print("Seleccione opción 1-4: ")
        option_type = int(input())
        print("")
        print("Spot con (.) para decimales: ")
        option_spot = float(input())
        print("")
        print("Strike con (.) para decimales: ")
        option_strike = float(input())
        print("")
        print("Tasa de Interés continua con (.) para decimales *100: ")
        option_rate = float(input()) / 100
        print("")
        print("Volatilidad  con (.) para decimales y *100: ")
        option_sd_risk = float(input()) / 100
        print("")
        print("Plazo en días: ")
        option_time_lenght = float(input())
        print("")
        print("Base del cálculo: ")
        option_base_lenght = float(input())
        print("")
        print("Número de Nodos : ")
        option_nodes_calc = float(input())
        option_time_years = option_time_lenght / option_base_lenght
        option_delta_time = option_time_years / option_nodes_calc

        self.data_valuationNeed = {"option_type": option_type, "option_spot": option_spot,
                                   "option_strike": option_strike, "option_rate": option_rate,
                                   "option_sd_risk": option_sd_risk, "option_time_years": option_time_years,
                                   "option_delta_time": option_delta_time, "option_nodes_calc": option_nodes_calc}
        print(self.data_valuationNeed)

    # Calculation of parameters of projection
    def parameters_calculation_binomial_case(self):
        projection_node_U = np.exp(
            np.sqrt(self.data_valuationNeed["option_delta_time"]) * self.data_valuationNeed["option_sd_risk"])
        projection_node_D = 1 / projection_node_U
        probability_factor = np.exp(
            self.data_valuationNeed["option_delta_time"] * self.data_valuationNeed["option_rate"])
        probability_calculation_success = (probability_factor - projection_node_D) / (
                projection_node_U - projection_node_D)
        probability_calculation_failure = 1 - probability_calculation_success
        discount_factor = 1 / probability_factor
        return [projection_node_U, projection_node_D, probability_factor, probability_calculation_success,
                probability_calculation_failure, discount_factor]

    def definition_binomial_tree_calculation(self):
        array_princpal_parametters = self.parameters_calculation_binomial_case()
        projection_spot_rate = self.creating_forward_tree(self.data_valuationNeed["option_nodes_calc"],
                                                          self.data_valuationNeed["option_spot"],
                                                          float(array_princpal_parametters[0]),float( array_princpal_parametters[1]))
        print("factor_up")
        print(array_princpal_parametters[0])
        print("factor_down")
        print(array_princpal_parametters[1])
        print("probability_up")
        print(array_princpal_parametters[3])
        print("probability_down")
        print(array_princpal_parametters[4])
        print("Discount Fact")
        print(array_princpal_parametters[5])
        
        arrayValuationGen=self.node_iterator_binomial_calculation(projection_spot_rate,
                                                                  self.data_valuationNeed["option_strike"],
                                                                  array_princpal_parametters[3],
                                                                  array_princpal_parametters[4],
                                                                  array_princpal_parametters[5],
                                                                  self.data_valuationNeed["option_nodes_calc"])
        print("option Valuation ->"+str(arrayValuationGen))
        
    # Projection of recombinant tree
    def creating_forward_tree(self, number_nodes, spot_rate, factor_u, factor_d):
        #print("".join((str(factor_u),"---",str(factor_d))))
        counter = 0
        matrix_factors_to_fill = [[0 for y in range(int(number_nodes)+1)] for x in range(int(number_nodes)+1)]
        for n in matrix_factors_to_fill:
            quantifier = lambda variable_n, projector: variable_n * projector
            if (counter == 0):
                n[0] = spot_rate
                for first_row_tree in range(len(n)-1):
                    n[first_row_tree + 1] = quantifier(n[first_row_tree], factor_u)
            else:
                for row_iterator in range(counter-1,len(n)-1):
                    n[row_iterator + 1] = quantifier(matrix_factors_to_fill[counter-1][row_iterator], factor_d)

            counter += 1

        return matrix_factors_to_fill

    #Creation of Matrix for calculation of option values
    def node_iterator_binomial_calculation(self,arraySpotsProjected,strike_no,prob_u,prob_d,discount_fact, numberNodes):
        value_t=lambda spot_op: np.max((spot_op-self.data_valuationNeed["option_strike"],0)) if(self.data_valuationNeed["option_type"]==1 or self.data_valuationNeed["option_type"]==3) else np.max((self.data_valuationNeed["option_strike"]-spot_op,0))
        matrix_factors_to_fill = [[[value_t(j) for j in y] for y in arraySpotsProjected] for x in arraySpotsProjected]
        matrix_factors_to_fill=np.array(matrix_factors_to_fill)
        matrix_factors_to_fill=np.reshape(matrix_factors_to_fill,(-1,numberNodes+1))
        matrix_factors_to_fill=matrix_factors_to_fill[:numberNodes+1]
        matrix_factors_to_fill=matrix_factors_to_fill[:,::-1]
        matrix_factors_to_fill=matrix_factors_to_fill.transpose()
        matrix_valuation=np.zeros((16,16))
        counter=0
        line_row=0
        for i in matrix_factors_to_fill:
            for j in i:
                if(counter<numberNodes and line_row>0):
                    prior_value_up=matrix_valuation[line_row-1,counter] 
                    prior_value_down=matrix_valuation[line_row-1,counter+1]
                    matrix_valuation[line_row,counter]=self.function_calculation_bin_Norm(self.data_valuationNeed["option_type"],prob_u,prob_d,prior_value_up,prior_value_down,discount_fact,j)
                else:
                    matrix_valuation[line_row,counter]=j
                counter+=1
            
            counter=0
            line_row+=1
        
        #Return of last part of the matrix
        finalValue=matrix_valuation[-1,]
        return finalValue[0]
        
                
    def function_calculation_bin_Norm(self,argument_ne,probability_up,probability_down,prior_value_up,prior_value_down,discount_factor,value_exchange):
        caculation_expected_value=(probability_up*prior_value_up+probability_down*prior_value_down)*discount_factor
        calcule_max_expected=np.max((caculation_expected_value,value_exchange)) if(argument_ne==3 or argument_ne==4) else  caculation_expected_value
        return calcule_max_expected