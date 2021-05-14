package com.redislab.hackathon.domain;

import lombok.Data;
import org.hibernate.annotations.GenericGenerator;

import javax.persistence.*;
import java.util.List;

@Data
@Entity
public class Customer {
    @Id
    @GeneratedValue(generator = "UUID")
    @GenericGenerator(name = "UUID", strategy = "org.hibernate.id.UUIDGenerator")
    private String id;
    private String name;
    private String email;
    private Integer age;
    private String mobile;
    private String gender;
    private String address;
    private String pincode;
    private String location;
    private Integer experience;
    @OneToMany(cascade = CascadeType.ALL, fetch = FetchType.EAGER)
    private List<Property> properties;
}
