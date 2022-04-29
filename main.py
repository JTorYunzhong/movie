import mode1_2
import word_visual
import KevinBacon


if __name__ == "__main__":
    '''
    ls = ["star wars", "iron man", "blade runner", "pulp fiction", "Fantastic Beasts", "batman","spider-man","dog", "sing", "dog","harry potter","hotel","peter","mask","american"]
    ls = ["101101 Rent Boys", "14 Million Dreams", "19","24 Hours","Strong","36 Hours","Aadmi","Aaghosh"]
    ls = ["Aaj","Aanchal","Aaron","Aas","Aashiq","Aau","Abana ","Abandoned","Abashiri","Abbott","ABC"]
    ls = ["Abdul","Abel","Abenteuer","Abgrund","Abhijaan ","Abhinava ","Abi", "Abilene","Abismo","Abla"]
    ls= ["Abo","Abominable","Abortion","About","Abran","Abre","Abrigo","Abry","Abschied","Absence","Absinthe"]
    ls =["Absolut","Absolute","Abu","Abuelo","Abuse","Abuso","Abyss","Academy","Acapulco","Accadde","Accent"]
    ls = ["Access","Accident","Accidental","According","Account","Accused","Ace","Achter","Achtung","Aci"]
    ls =["Acid","Acosada","Acrobate","Across","Act","Action","Actors","Actress","Ada","Adam","Addict"]
    ls = ["Addio","Addio","1,000 Reward","A","Cross","Gator","I","If","In","Ostler","tags","till","this"] 
    ls = ["Twas","10","100","1000","12","13","15","1998","2","20","21","22","24","hours","down"] 
    ls = ["29", "2nd","3","30","300","4","tokens","card","finger","car","lesson","6","5"] 
    ls = ["7","8","9","la","age","Aaj","Aan","ABC","Abduction","Abenteuer","About","Face"]
    ls= ["above","upside","defense","walk","cloud","distance","peter","mission","woman","world","war"]
    ls=["animal","seed","fight","battle","charing","scent","singing","house","aparment","slide","seek"]# not run
    ls=["island","muse","drink","shark","cat","dog","mouse","bird","frog","frost","togo","friend"]
    ls = ["Absolute","reward","pent","bear","bad","breaker","cross","foxy","G","fired","men","bait"]
    ls=["hotel","homunculus","hong kong","honest","honey","honeymoon","hong","honor","family","Gelbe"]
    ls =["Geliebte","gem","Gemini", "Gen","Gendai","General","wonder","batman","super man","vampire"]
    ls=["Along With","Parasite ","Belladonna","Terminator","Rome","The Last","Rashomon","Finch","music"]
    ls=["Ashes","Christmas","hero","Another Round","last","drunk","Newton","Dark Water","hacker"]
    ls=["Manchester By The Sea","girl","soul","alone","Just Before I Go","exit","Kiki's Delivery Service","Senden Bana Kalan"]
    '''
    #ls=["a trip","On The Basis Of Sex","Synchronic","Cutie And The Boxer","Life Is Beautiful","Raazi","The Scribbler"]
    #ls =["Australia","Birth","Cold Mountain","The Beguiled","The Paperboy","Strangerland"]
    #mode1_2.load_data(ls)

    while True:
        print("There are four mode to choose from. Mode 1 is to input a string then you get a series of related movie titles about you input")
        print("In mode 2, you will get movie recommendation according to IMDb score about the results you get from mode 1. So you have to finish mode 1 to get into mode 2")
        print("In mode 3, you will get a word cloud iamage about the plots of the movies you serched beafore. Bigger fond represent higher frequency")
        print("In mode 4, you need to input two names of actor or actress. Then you can get ")

        user_input = input("Please select: 'mode 1', 'mode 3', 'mode 4' or 'quit' to continue. --")
        if user_input == "quit":
            print("Thanks for using. Bye!")
            break
        elif user_input == "mode 1":
            ls_title = None
            while True:
                print("Please input a single string or a couple of strings, separated by / like A/B/C")     
                print("Related movie names would be print out about your input.")
                print("or enter mode 2 to enter mode 2")
                print("Or enter quit to return to previous menu" )
                val = input("--")
                if val == "quit":
                    break
                elif val == "mode 2":
                    if ls_title != None:
                        print("Movie recommendation according to IMDb rating:")
                        mode1_2.get_sorted_recommendations(ls_title)
                    else:
                        print("Please search movie first before enter mode 2")
                else:
                    val = val.split("/")
                    if len(val) < 1:
                        print("Invalid input. Please enter again.")
                        continue
                    else:
                        ls_input = [i.strip() for i in val]
                        ls_title = mode1_2.get_related_titles(ls_input)
                        print("Related movie title:",ls_title)
                
        elif user_input == "mode 3":
            word_visual.visual()
        elif user_input == "mode 4":
            KevinBacon.run()
        else:
            print("Invalid input. Please read instructions provided below and enter again")
