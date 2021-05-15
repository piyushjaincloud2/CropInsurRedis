package com.redislab.hackathon.service;

import com.redislab.hackathon.domain.*;
import com.redislab.hackathon.repository.ClaimRepository;
import com.redislab.hackathon.repository.CustomerRepository;
import com.redislab.hackathon.repository.InspectionRepository;
import com.redislab.hackathon.repository.PolicyRepository;
import com.redislab.hackathon.util.ResponseDto;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.*;

@Service
public class PolicyService {
    @Autowired
    private PolicyRepository policyRepository;
    @Autowired
    private CustomerRepository customerRepository;
    @Autowired
    private ClaimRepository claimRepository;
    @Autowired
    private PropertyRepository propertyRepository;
    @Autowired
    private InspectionRepository inspectionRepository;

    public ResponseDto save(Policy policy) {
        Customer customer = customerRepository.findById(policy.getCustomerId()).get();
        Property property = customer.getProperties().stream()
                .filter(it -> it.getId().equals(policy.getPropertyId())).findFirst().get();
        Inspection inspection = inspectionRepository.findById(policy.getInspectionId()).get();
        Map<String, Double> calculateMap = calculateHarvest(property, getAverage(inspection.getFieldDataList()));
        policy.setPolicyPremium(calculateMap.get("preHarvestPremium"));
        policy.setPolicySumAssured(calculateMap.get("preHarvestIdv"));
        policyRepository.save(policy);
        property.setPolicy(policy);
        propertyRepository.save(property);
        return ResponseDto.builder().status(true).data(policy).message("Policy is Saved Successfully").build();
    }

    private Map<String, Double> getAverage(List<FieldData> fields) {

        Double cultivatedLand = fields.parallelStream().mapToLong(it -> it.getCultivatedLand().longValue()).average().getAsDouble();
        Double highQualityCrop = fields.parallelStream().mapToLong(it -> it.getHighQualityCrop().longValue()).average().getAsDouble();
        Double lowQualityCrop = fields.parallelStream().mapToLong(it -> it.getLowQualityCrop().longValue()).average().getAsDouble();
        Map<String, Double> map = new HashMap<>();
        map.put("cultivatedLand", cultivatedLand);
        map.put("highQualityCrop", highQualityCrop);
        map.put("lowQualityCrop", lowQualityCrop);
        return map;
    }

    public Map calculateHarvest(Property property, Map<String, Double> map) {
        Double cultivatedLand = map.get("cultivatedLand");
        Double highQualityCrop = map.get("highQualityCrop");
        Double lowQualityCrop = map.get("lowQualityCrop");
        BigDecimal rate = Objects.nonNull(property.getPremiumRate()) ? property.getPremiumRate() : new BigDecimal(2);
        double baseIdv = getBaseIDV(property);
        double preHarvestIdv = baseIdv * cultivatedLand / 100;
        double premium = (rate.doubleValue() / 100) * preHarvestIdv;
        double postHarvestIdv = (baseIdv * highQualityCrop / 100) + (baseIdv * lowQualityCrop / 100) * 0.5;
        Map<String, Double> response = new HashMap<>();
        response.put("baseIdv", roundOff(baseIdv));
        response.put("preHarvestIdv", roundOff(preHarvestIdv));
        response.put("postHarvestIdv", roundOff(postHarvestIdv));
        response.put("preHarvestPremium", roundOff(premium));
        return response;
    }

    private double roundOff(double num) {
        return Math.round(num * 100) / 100;

    }

    private double getBaseIDV(Property property) {
        long baseIdv = property.getFarmArea().longValue() * property.getExpectedMarketPrice().longValue() * property.getExpectedYeild().longValue() * 100L;
        return roundOff(baseIdv);
    }

    public ResponseDto claim(Claim claim) {
        Property property = propertyRepository.findById(claim.getPropertyId()).get();
        Policy policy = policyRepository.findById(property.getPolicy().getId()).get();
        Inspection inspection = inspectionRepository.findById(claim.getInspectionId()).get();
        Map<String, Double> calculateMap = calculateHarvest(property, getAverage(inspection.getFieldDataList()));
        policy.setClaimPremium(calculateMap.get("preHarvestPremium"));
        policy.setClaimAmount(calculateMap.get("preHarvestIdv"));
        policyRepository.save(policy);
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
