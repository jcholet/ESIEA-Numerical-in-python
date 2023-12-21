echo "---------------------"
echo "---------TABU--------"
echo "---------------------"

for i in {1..10}; do
    fichier="../Instances/larges/large$i.txt"
    echo "Fichier $i"
    for i in {1..5}; do
        echo "Itération $i"
        python3 ../tabu_search.py 120 $fichier
        wait
    done
done

echo "---------------------"
echo "---------ACO---------"
echo "---------------------"

for i in {1..10}; do
    fichier="../Instances/larges/large$i.txt"
    echo "Fichier $i"
    for i in {1..5}; do
        echo "Itération $i"
        python3 ../aco.py 120 $fichier
        wait
    done
done

echo "---------------------"
echo "---------GEN---------"
echo "---------------------"

for i in {1..10}; do
    fichier="../Instances/larges/large$i.txt"
    echo "Fichier $i"
    for i in {1..5}; do
        echo "Itération $i"
        python3 ../genetic.py 120 $fichier
        wait
    done
done

echo "---------------------"
echo "---------GTA---------"
echo "---------------------"

for i in {1..10}; do
    fichier="../Instances/larges/large$i.txt"
    echo "Fichier $i"
    for i in {1..5}; do
        echo "Itération $i"
        python3 ../genetic_with_tabu.py 120 $fichier
        wait
    done
done