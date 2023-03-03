package com.example.api.Controllers;

import com.example.api.Entities.User;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CookieValue;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class UserController {
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
}
