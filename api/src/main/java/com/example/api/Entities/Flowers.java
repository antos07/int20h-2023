package com.example.api.Entities;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.ArrayList;
import java.util.List;

@Document
public class Flowers {
    @Id
    public int id;
    public List<String> flowers=new ArrayList<>();

    public Flowers(int id) {
        this.id =id;
    }
}
