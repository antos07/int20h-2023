package com.example.api.Controllers;

import com.example.api.Configurations.SimpleMongoConfig;
import com.example.api.Entities.Flowers;
import com.example.api.Entities.User;
import com.example.api.Repositories.FlowersRepository;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CookieValue;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class UserController {
    @Autowired
    FlowersRepository flowersRepository;
    @GetMapping("/setCookie")
    public ResponseEntity<?> setCookie(HttpServletResponse response){
        User user=new User();
        Cookie cookie = new Cookie("id", Integer.toString(user.getId()));
        cookie.setPath("/");
        cookie.setMaxAge(86400);
        response.addCookie(cookie);
        response.setContentType("text/plain");
        return ResponseEntity.ok().body(HttpStatus.OK);
    }
    @GetMapping(value = "/getCookie")
    public ResponseEntity<?> readCookie(@CookieValue(value = "id") String data) {
        return ResponseEntity.ok().body(data);
    }
    @GetMapping("/save1")
    public void save1(@CookieValue(value = "Id") String data){
        Flowers flowers=new Flowers(Integer.parseInt(data));
        flowersRepository.save(flowers);
    }
    @GetMapping("/save/{name}")
    public void save(@CookieValue(value = "Id") String data, @PathVariable String name){
        int id=Integer.parseInt(data);
        SimpleMongoConfig simpleMongoConfig=new SimpleMongoConfig();
        Flowers temFlowers=simpleMongoConfig.mongoTemplate().findById(id, Flowers.class);
        temFlowers.flowers.add(name);
    }
    @GetMapping("/find")
    public Flowers find(@CookieValue(value = "Id") String data){
        int id=Integer.parseInt(data);
        SimpleMongoConfig simpleMongoConfig=new SimpleMongoConfig();
        Flowers temFlowers=simpleMongoConfig.mongoTemplate().findById(id, Flowers.class);
        return temFlowers;
    }
}
