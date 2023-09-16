package com.company;

import java.io.File;
import java.nio.file.Files;
import java.util.ArrayList;
import java.nio.file.Paths;
import java.io.FileNotFoundException;  // Import this class to handle errors
import java.util.Scanner; // Import the Scanner class to read text files

public class Simulation {

    static ArrayList loadItems(String textFile) {

        ArrayList liste = new ArrayList();
        try{
            File myObj = new File(textFile);
            Scanner myReader = new Scanner(myObj);
            while (myReader.hasNextLine()) {
                String data = myReader.nextLine();
                liste.add(data);
        }
            myReader.close() ;
     }
        catch (FileNotFoundException e) {
             System.out.println("An error occurred.");
             e.printStackTrace();
        }
        Object[] liste2 = liste.toArray();
        ArrayList<Item> items = new ArrayList();
        int i;
        for (i=0; i< liste.size(); i++){
            String[] item = liste2[i].toString().split(",",4);
            items.add(new Item(item[0],Integer.parseInt(item[1]),Integer.parseInt(item[2]),Integer.parseInt(item[3])));
        }

     return items;


    }

    static ArrayList loadU1(ArrayList<Item> loadedItems){
        ArrayList<U1> rockets = new ArrayList();

        int i = 0;
        int k=0;
        rockets.add(new U1());
        for (i=0; i< loadedItems.size(); i++){
            if (rockets.get(k).canCarry(loadedItems.get(i))){

                rockets.get(k).carry(loadedItems.get(i));
            }
            else{
                k++;
                rockets.add(new U1());
                rockets.get(k).carry(loadedItems.get(i));

            }
        }
        return rockets;
    }

    static ArrayList loadU2(ArrayList<Item> loadedItems){
        ArrayList<U2> rockets = new ArrayList();

        int i = 0;
        int k=0;
        rockets.add(new U2());
        for (i=0; i< loadedItems.size(); i++){
            if (rockets.get(k).canCarry(loadedItems.get(i))){
                rockets.get(k).carry(loadedItems.get(i));
            }
            else{
                k++;
                rockets.add(new U2());
                rockets.get(k).carry(loadedItems.get(i));
            }
        }
        return rockets;
    }

    static ArrayList loadUall(ArrayList<Item> loadedItems, int carryWeight, double launch, double landing ){
        ArrayList<Uall> rockets = new ArrayList();

        int i = 0;
        int k=0;
        rockets.add(new Uall(carryWeight, launch, landing));
        for (i=0; i< loadedItems.size(); i++){
            if (rockets.get(k).canCarry(loadedItems.get(i))){

                rockets.get(k).carry(loadedItems.get(i));
            }
            else{
                k++;
                rockets.add(new Uall(carryWeight, launch, landing));
                rockets.get(k).carry(loadedItems.get(i));
            }
        }
        return rockets;
    }

    static ArrayList<Integer> runSimulation(ArrayList<Rocket> rockets){
        int totalPrice = 0;
        int lifePrice = 0;
        int i;
        ArrayList r = new ArrayList();

        for (i=0;i< rockets.size();i++){
            totalPrice += rockets.get(i).cost;
            totalPrice += rockets.get(i).carryCost;
            while (!rockets.get(i).launch() || !rockets.get(i).landing()){
                totalPrice += rockets.get(i).cost;
                totalPrice += rockets.get(i).carryCost;
                lifePrice += rockets.get(i).lifeCost;
            }
        }
        r.add(totalPrice);
        r.add(lifePrice);
        return (r);
    }







}
