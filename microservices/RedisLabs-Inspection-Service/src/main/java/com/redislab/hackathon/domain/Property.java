package com.redislab.hackathon.domain;

import lombok.Data;
import org.hibernate.annotations.GenericGenerator;

import javax.persistence.*;
import java.math.BigDecimal;
import java.util.List;

@Data
@Entity
public class Property {
    @Id
    @GeneratedValue(generator = "UUID")
    @GenericGenerator(name = "UUID", strategy = "org.hibernate.id.UUIDGenerator")
    private String id;
    private String cropName;
    private Integer cropDuration;
    private BigDecimal premiumRate;
    private BigDecimal farmArea;
    private BigDecimal expectedYeild;
    private BigDecimal expectedMarketPrice;
    private BigDecimal coveragePeriod;
    private String latitude;
    private String longitude;
    @OneToOne
    private Policy policy;
    @OneToMany(cascade = CascadeType.ALL, fetch = FetchType.EAGER)
    private List<Inspection> inspections;
}
