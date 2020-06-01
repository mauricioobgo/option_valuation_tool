from class_valuation_calculus import valuation_calculus as valuation


# Método main para ejecución de valoración
# nuevo método
def main():
    variable_iterate_process = True
    valuation_object = valuation()
    while (variable_iterate_process == True):
        #valuation_object.construct_info_need_valuate()
        valuation_object.parameters_calculation_binomial_case()
        valuation_object.definition_binomial_tree_calculation()
        # new_changes
        print("Desea continuar valorando opciones (SI/NO): ")
        response_question_continue = input()
        if (str(response_question_continue).upper().strip() != "SI"):
            variable_iterate_process = False


if __name__ == '__main__':
    main()
