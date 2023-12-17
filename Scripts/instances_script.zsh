#!/bin/zsh

echo "Exécution de l'instance 1"
glpsol --lp instance1.lp --output solution_instance1.txt
wait

echo "Exécution de l'instance 2"
glpsol --lp instance2.lp --output solution_instance2.txt
wait

echo "Exécution de l'instance 3"
glpsol --lp instance3.lp --output solution_instance3.txt
wait


echo "Exécution de l'instance 4"
glpsol --lp instance4.lp --output solution_instance4.txt
wait


echo "Exécution de l'instance 5"
glpsol --lp instance5.lp --output solution_instance5.txt
wait


echo "Exécution de l'instance 6"
glpsol --lp instance6.lp --output solution_instance6.txt
wait


echo "Exécution de l'instance 7"
glpsol --lp instance7.lp --output solution_instance7.txt
wait


echo "Exécution de l'instance 8"
glpsol --lp instance8.lp --output solution_instance8.txt
wait


echo "Exécution de l'instance 9"
glpsol --lp instance9.lp --output solution_instance9.txt
wait


echo "Exécution de l'instance 10"
glpsol --lp instance10.lp --output solution_instance10.txt
wait