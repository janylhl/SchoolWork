package com.company;

public class U1 extends Rocket {

    public U1(){
        this.Weight = 10000;
        this.maxWeight = 18000;
        this.cost = 100000000;
        this.launchExplosion = 0.05;
        this.landingCrash = 0.01;

    }
    double probaLanding(){
        return (Math.pow((Weight / maxWeight),3) * landingCrash);
    }
    double probaLaunching(){
        return (Math.pow((Weight / maxWeight),3) * launchExplosion);
    }

    @Override
    public boolean landing() {
        double x = Math.random();
        if (x < probaLanding()) {
            return false;
        } else {
            return true;
        }
    }

    @Override
    public boolean launch() {
        double x = Math.random();
        if (x < probaLaunching()) {
            return false;
        } else {
            return true;
        }
    }

}

