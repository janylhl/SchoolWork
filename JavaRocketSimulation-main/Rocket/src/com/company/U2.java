package com.company;


public class U2<Rock> extends Rocket {

    public U2(){
        this.Weight = 18000;
        this.maxWeight = 29000;
        this.cost = 120000000;
        this.launchExplosion = 0.04;
        this.landingCrash = 0.08;
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

