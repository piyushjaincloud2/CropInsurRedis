package com.redislab.hackathon.repository;

import com.redislab.hackathon.domain.Inspection;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface InspectionRepository extends JpaRepository<Inspection, String> {
    List<Inspection> findAllByCustomerId(String customerId);
}
