package com.redislab.hackathon.repository;

import com.redislab.hackathon.domain.FieldData;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface FieldDataRepository extends JpaRepository<FieldData, String> {
}
