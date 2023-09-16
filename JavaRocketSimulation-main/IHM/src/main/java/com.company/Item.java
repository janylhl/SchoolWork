package com.company;

public class Item {

    public String getName() {
        return Name;
    }

    public void setName(String name) {
        Name = name;
    }

    public int getWeight() {
        return Weight;
    }

    public void setWeight(int weight) {
        Weight = weight;
    }

    public int getCost() {
        return Cost;
    }

    public void setCost(int cost) {
        Cost = cost;
    }

    public int getLife() {
        return Life;
    }

    public void setLife(int life) {
        Life = life;
    }

    String Name;

    int Weight;

    int Cost;

    int Life;

    public Item( String Name, int Weight, int Cost, int Life){
        this.Name = Name;
        this.Weight = Weight;
        this.Cost = Cost;
        this.Life = Life;
    }



}
