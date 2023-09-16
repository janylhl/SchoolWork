package com.company;



public interface Spaceship {

    boolean launch() ;

    boolean landing() ;

    boolean canCarry(Item a, int remplissage) ;

    void carry(Item a) ;

}
