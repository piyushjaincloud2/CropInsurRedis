package com.redislab.hackathon.repository;

import com.redislab.hackathon.domain.Customer;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository("CustomerRepository")
public interface CustomerRepository extends JpaRepository<Customer, String> {
}
