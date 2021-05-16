package com.redislab.hackathon.repository;

import com.redislab.hackathon.domain.Claim;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ClaimRepository extends JpaRepository<Claim,String> {
}
