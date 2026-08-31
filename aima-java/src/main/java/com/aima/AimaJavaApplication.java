package com.aima;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class AimaJavaApplication {

    public static void main(String[] args) {
        SpringApplication.run(AimaJavaApplication.class, args);
    }

}
