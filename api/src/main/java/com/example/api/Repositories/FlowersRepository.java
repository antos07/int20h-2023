package com.example.api.Repositories;

import com.example.api.Entities.Flowers;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface FlowersRepository extends MongoRepository<Flowers, Integer> {
}
