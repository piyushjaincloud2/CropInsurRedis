package com.redislab.hackathon.service;

import com.redislab.hackathon.domain.Claim;
import com.redislab.hackathon.domain.Customer;
import com.redislab.hackathon.domain.Policy;
import com.redislab.hackathon.domain.Property;
import com.redislab.hackathon.repository.ClaimRepository;
import com.redislab.hackathon.repository.CustomerRepository;
import com.redislab.hackathon.repository.PolicyRepository;
import com.redislab.hackathon.util.ResponseDto;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class PolicyService {
    @Autowired
    private PolicyRepository policyRepository;
    @Autowired
    CustomerRepository customerRepository;
    @Autowired
    ClaimRepository claimRepository;
    @Autowired
    PropertyRepository propertyRepository;


    public ResponseDto save(Policy policy) {
        Customer customer = customerRepository.findById(policy.getCustomerId()).get();
        Property property = customer.getProperties().stream()
                .filter(it -> it.getId().equals(policy.getPropertyId())).findFirst().get();
        policyRepository.save(policy);
        property.setPolicy(policy);
        propertyRepository.save(property);
        return ResponseDto.builder().status(true).data(policy).message("Policy is Saved Successfully").build();
    }

    public ResponseDto claim(Claim claim) {
        claim = claimRepository.save(claim);
        return ResponseDto.builder().status(true).data(claim).message("Policy is Saved Successfully").build();
    }

    public ResponseDto get(String id) {
        Optional<Policy> optional = policyRepository.findById(id);
        return ResponseDto.builder().status(true).data(optional.get()).build();
    }

    public ResponseDto delete(String id) {
        policyRepository.deleteById(id);
        return ResponseDto.builder().status(true).message("Policy is deleted successfully").build();
    }

    public ResponseDto delete() {
        policyRepository.deleteAll();
        return ResponseDto.builder().status(true).message("Policy is deleted successfully").build();
    }
}
