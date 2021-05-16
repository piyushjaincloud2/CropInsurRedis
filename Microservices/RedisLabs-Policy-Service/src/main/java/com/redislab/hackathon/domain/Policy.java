package com.redislab.hackathon.domain;

import lombok.Data;
import org.hibernate.annotations.GenericGenerator;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import java.math.BigDecimal;
import java.util.Date;

@Data
@Entity
public class Policy {
    @Id
    @GeneratedValue(generator = "UUID")
    @GenericGenerator(name = "UUID", strategy = "org.hibernate.id.UUIDGenerator")
    private String id;
    private String inspectionId;
    private String propertyId;
    private String customerId;
    private Double policySumAssured;
    private Double policyPremium;
    private Double claimAmount;
    private Double claimPremium;
    private Date date = new Date();
}
