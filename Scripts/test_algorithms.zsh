echo "---------------------"
echo "---------TABU--------"
echo "---------------------"
for fichier in Instances/small/*.txt; do
    echo $fichier
    python3 tabu_search.py $fichier
    wait
    if [[ $fichier == *"instance19.txt"* ]]; then
        echo "Arrêt après avoir traité instance10.txt"
        break  # Interrompt la boucle
    fi
done

# for fichier in Instances/larges/*.txt; do
#     echo $fichier
#     python3 tabu_search.py $fichier
# done

echo "---------------------"
echo "---------ACO---------"
echo "---------------------"

for fichier in Instances/small/*.txt; do
    echo $fichier
    python3 aco.py 60 $fichier
    wait
    if [[ $fichier == *"instance19.txt"* ]]; then
        echo "Arrêt après avoir traité instance10.txt"
        break  # Interrompt la boucle
    fi
done

# for fichier in Instances/larges/*.txt; do
#     echo $fichier
#     python3 tabu_search.py $fichier
# done

echo "---------------------"
echo "---------GEN---------"
echo "---------------------"

for fichier in Instances/small/*.txt; do
    echo $fichier
    python3 genetic.py 60 $fichier
    wait
    if [[ $fichier == *"instance19.txt"* ]]; then
        echo "Arrêt après avoir traité instance10.txt"
        break  # Interrompt la boucle
    fi
done

# for fichier in Instances/larges/*.txt; do
#     echo $fichier
#     python3 genetic.py $fichier
# done

echo "---------------------"
echo "---------GTA---------"
echo "---------------------"

for fichier in Instances/small/*.txt; do
    echo $fichier
    python3 mabite.py 60 $fichier
    wait
    if [[ $fichier == *"instance19.txt"* ]]; then
        echo "Arrêt après avoir traité instance10.txt"
        break  # Interrompt la boucle
    fi
done

# for fichier in Instances/larges/*.txt; do
#     echo $fichier
#     python3 mabite.py $fichier
#     wait
# done