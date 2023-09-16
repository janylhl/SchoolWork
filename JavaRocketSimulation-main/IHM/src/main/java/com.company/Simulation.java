package com.company;

import java.io.File;
import java.nio.file.Files;
import java.util.ArrayList;
import java.nio.file.Paths;
import java.io.FileNotFoundException;  // Import this class to handle errors
import java.util.Scanner; // Import the Scanner class to read text files

public class Simulation {

    public static ArrayList loadItems(String textFile) {

        ArrayList liste = new ArrayList();
        try {
            File myObj = new File(textFile);
            Scanner myReader = new Scanner(myObj);
            while (myReader.hasNextLine()) {
                String data = myReader.nextLine();
                liste.add(data);
            }
            myReader.close();
        } catch (FileNotFoundException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
        Object[] liste2 = liste.toArray();
        ArrayList<Item> items = new ArrayList();
        int i;
        for (i = 0; i < liste.size(); i++) {
            String[] item = liste2[i].toString().split(",", 4);
            items.add(new Item(item[0], Integer.parseInt(item[1]), Integer.parseInt(item[2]), Integer.parseInt(item[3])));
        }

        return items;


    }

    static ArrayList loadU1(ArrayList<Item> loadedItems, int remplissage) {
        ArrayList<U1> rockets = new ArrayList();

        int i = 0;
        int k = 0;
        rockets.add(new U1());
        for (i = 0; i < loadedItems.size(); i++) {
            if (rockets.get(k).canCarry(loadedItems.get(i), remplissage)) {

                rockets.get(k).carry(loadedItems.get(i));
            } else {
                k++;
                rockets.add(new U1());
                rockets.get(k).carry(loadedItems.get(i));

            }
        }
        return rockets;
    }

    static ArrayList loadU2(ArrayList<Item> loadedItems, int remplissage) {
        ArrayList<U2> rockets = new ArrayList();

        int i = 0;
        int k = 0;
        rockets.add(new U2());
        for (i = 0; i < loadedItems.size(); i++) {
            if (rockets.get(k).canCarry(loadedItems.get(i), remplissage)) {
                rockets.get(k).carry(loadedItems.get(i));
            } else {
                k++;
                rockets.add(new U2());
                rockets.get(k).carry(loadedItems.get(i));
            }
        }
        return rockets;
    }

    static ArrayList loadUall(ArrayList<Item> loadedItems, int carryWeight, double launch, double landing, int remplissage) {
        ArrayList<Uall> rockets = new ArrayList();

        int i = 0;
        int k = 0;
        rockets.add(new Uall(carryWeight, launch, landing));
        for (i = 0; i < loadedItems.size(); i++) {
            if (rockets.get(k).canCarry(loadedItems.get(i), remplissage)) {

                rockets.get(k).carry(loadedItems.get(i));
            } else {
                k++;
                rockets.add(new Uall(carryWeight, launch, landing));
                rockets.get(k).carry(loadedItems.get(i));
            }
        }
        return rockets;
    }

    static ArrayList<Integer> runSimulation(ArrayList<Rocket> rockets) {
        long totalPrice = 0;
        int lifePrice = 0;
        int i;
        ArrayList r = new ArrayList();
        int k =0;

        for (i = 0; i < rockets.size(); i++) {
            totalPrice += rockets.get(i).cost;
            totalPrice += rockets.get(i).carryCost;
            k++;
            while (!rockets.get(i).launch() || !rockets.get(i).landing()) {
                totalPrice += rockets.get(i).cost;
                totalPrice += rockets.get(i).carryCost;
                lifePrice += rockets.get(i).lifeCost;
                k++;
            }
        }
        r.add(totalPrice);
        r.add(lifePrice);
        r.add(k);
        return (r);
    }


    static public ArrayList SimulateU1(String phase, int remplissage) {

        ArrayList Rturn = new ArrayList();
        ArrayList phase_1 = Simulation.loadItems(phase);
        ArrayList U1_phase_1 = Simulation.loadU1(phase_1, remplissage);


        ArrayList<Integer> X = new ArrayList<Integer>();
        ArrayList Y = new ArrayList();
        int i;
        for (i = 0; i < 40; i++) {
            X.add((int) i * 100);
            Y.add(0);
        }
        int nbrIterations = 100000;
        i = 0;
        long cost = 0;
        long lifeCost = 0;
        long nbrFusees = 0;
        for (i = 0; i < nbrIterations; i++) {
            ArrayList R = Simulation.runSimulation(U1_phase_1);
            long kk =  (long)R.get(0) / ((long)100000000);
            int k = (int)kk;
            Y.set(k, (int) Y.get(k) + 1);
            cost += (long) R.get(0);
            lifeCost += (int) R.get(1);
            nbrFusees += (int) R.get(2);
        }
        long avgCost = cost/nbrIterations;


        Rturn.add(X);
        Rturn.add(Y);
        Rturn.add((int) avgCost);
        Rturn.add((int)(lifeCost / nbrIterations));
        Rturn.add(nbrIterations);
        Rturn.add((int)(nbrFusees/nbrIterations));

        return Rturn;
    }

    static public ArrayList SimulateU2(String phase, int remplissage) {

        ArrayList Rturn = new ArrayList();
        ArrayList phase_1 = Simulation.loadItems(phase);
        ArrayList U1_phase_1 = Simulation.loadU2(phase_1, remplissage);


        ArrayList<Long> X = new ArrayList<Long>();
        ArrayList Y = new ArrayList();
        int i;
        for (i = 0; i < 40; i++) {
            X.add((long) i * 100000000);
            Y.add(0);
        }
        int nbrIterations = 100000;
        i = 0;
        long cost = 0;
        long lifeCost = 0;
        long nbrFusees = 0;
        for (i = 0; i < nbrIterations; i++) {
            ArrayList R = Simulation.runSimulation(U1_phase_1);
            long kk =  (long)R.get(0) / ((long)100000000);
            int k = (int)kk;
            Y.set(k, (int) Y.get(k) + 1);
            cost += (long) R.get(0);
            lifeCost += (int) R.get(1);
            nbrFusees += (int) R.get(2);
        }
        long avgCost = cost/nbrIterations;


        Rturn.add(X);
        Rturn.add(Y);
        Rturn.add((int) avgCost);
        Rturn.add((int)(lifeCost / nbrIterations));
        Rturn.add(nbrIterations);
        Rturn.add((int)(nbrFusees/nbrIterations));

        return Rturn;

    }


    static public ArrayList SimulateUall(String phase, int carryWeight, double launch, double landing, int remplissage) {
        double launchV = launch / 100;
        double landingV = landing / 100;
        ArrayList Rturn = new ArrayList();
        ArrayList phase_1 = Simulation.loadItems(phase);
        ArrayList U1_phase_1 = Simulation.loadUall(phase_1, carryWeight, launchV, landingV, remplissage);


        ArrayList<Long> X = new ArrayList<Long>();
        ArrayList Y = new ArrayList();
        int i;
        for (i = 0; i < 150; i++) {
            X.add((long) i * 100000000);
            Y.add(0);
        }
        int nbrIterations = 100000;
        i = 0;
        long cost = 0;
        long lifeCost = 0;
        long nbrFusees = 0;
        for (i = 0; i < nbrIterations; i++) {
            ArrayList R = Simulation.runSimulation(U1_phase_1);
            long kk =  (long)R.get(0) / ((long)10000000);
            int k = (int)kk;
            Y.set(k, (int) Y.get(k) + 1);
            cost += (long) R.get(0);
            lifeCost += (int) R.get(1);
            nbrFusees += (int) R.get(2);
        }
        long avgCost = cost/nbrIterations;


        Rturn.add(X);
        Rturn.add(Y);
        Rturn.add((int) avgCost);
        Rturn.add((int)(lifeCost / nbrIterations));
        Rturn.add(nbrIterations);
        Rturn.add((int)(nbrFusees/nbrIterations));

        return Rturn;
    }

}









