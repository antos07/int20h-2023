package com.example.api.Entities;

import java.util.Random;

public class User {
    private int id;

    public void setId(int id) {
        this.id = id;
    }

    public int getId() {
        return id;
    }

    public User() {
        Random rn = new Random();
        this.id=-1;
        while(this.id<0)
            this.id =rn.nextInt();
    }
}
