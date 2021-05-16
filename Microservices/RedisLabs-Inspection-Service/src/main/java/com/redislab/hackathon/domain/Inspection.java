package com.redislab.hackathon.domain;

import lombok.Data;
import org.hibernate.annotations.LazyCollection;
import org.hibernate.annotations.LazyCollectionOption;
import org.springframework.format.annotation.DateTimeFormat;

import javax.persistence.CascadeType;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.OneToMany;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

@Data
@Entity
public class Inspection implements Serializable {
    @Id
    private String id;
    private String propertyId;
    private String customerId;
    private Double preHarvestPremium;
    private Double postHarvestIdv;
    private Double preHarvestIdv;
    @DateTimeFormat(pattern = "dd-MM-yyyy")
    private Date date;
    @OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)
    @LazyCollection(LazyCollectionOption.FALSE)
    private List<FieldData> fieldDataList = new ArrayList<>();
}
