package com.redislab.hackathon.domain;

import lombok.Data;
import org.hibernate.annotations.GenericGenerator;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import java.io.Serializable;
import java.math.BigDecimal;

@Data
@Entity
public class FieldData implements Serializable {
    @GeneratedValue(generator = "UUID")
    @GenericGenerator(name = "UUID", strategy = "org.hibernate.id.UUIDGenerator")
    @Id
    private String id;
    private String fileName;
    private String weather;
    private BigDecimal windSpeed;
    private BigDecimal cultivatedLand;
    private BigDecimal damageArea;
    private BigDecimal highQualityCrop;
    private BigDecimal lowQualityCrop;
    private BigDecimal other;
    private BigDecimal inFertileLand;
    private BigDecimal water;
    private boolean isDone;
}
