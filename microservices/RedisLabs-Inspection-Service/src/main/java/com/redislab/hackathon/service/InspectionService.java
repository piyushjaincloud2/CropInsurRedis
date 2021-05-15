package com.redislab.hackathon.service;

import com.redislab.hackathon.domain.Customer;
import com.redislab.hackathon.domain.FieldData;
import com.redislab.hackathon.domain.Inspection;
import com.redislab.hackathon.domain.Property;
import com.redislab.hackathon.repository.CustomerRepository;
import com.redislab.hackathon.repository.FieldDataRepository;
import com.redislab.hackathon.repository.InspectionRepository;
import com.redislab.hackathon.repository.PolicyRepository;
import com.redislab.hackathon.util.ResponseDto;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

import java.math.BigDecimal;
import java.util.*;

@Service
public class InspectionService {
    @Autowired
    private FieldDataRepository fieldDataRepository;
    @Autowired
    private InspectionRepository inspectionRepository;
    @Autowired
    PolicyRepository policyRepository;
    @Autowired
    CustomerRepository customerRepository;

    public ResponseDto save(Inspection inspection) {
        Customer customer = customerRepository.findById(inspection.getCustomerId()).get();
        Property property = customer.getProperties().stream().filter(it -> it.getId().equals(inspection.getPropertyId())).findFirst().get();
        List<Inspection> inspections = CollectionUtils.isEmpty(property.getInspections()) ? new ArrayList<>() : property.getInspections();
        Map<String, Double> calculateMap = calculateHarvest(property, getAverage(inspection.getFieldDataList()));
        inspection.setPostHarvestIdv(calculateMap.get("postHarvestIdv"));
        inspection.setPreHarvestIdv(calculateMap.get("preHarvestIdv"));
        inspection.setPreHarvestPremium(calculateMap.get("preHarvestPremium"));
        inspections.add(inspection);
        property.setInspections(inspections);
        customerRepository.save(customer);
        Map<String, Object> response = new HashMap<>();
        response.put("inspectionId", inspection.getId());
        response.putAll(calculateMap);
        return ResponseDto.builder().status(true).data(response).message("Inspection is Created Successfully").build();
    }


    private Map<String, Double> getAverage(List<FieldData> fields) {

        Double cultivatedLand = fields.parallelStream().mapToLong(it -> it.getCultivatedLand().longValue()).average().getAsDouble();
        Double damageArea = fields.parallelStream().mapToLong(it -> it.getDamageArea().longValue()).average().getAsDouble();
        Double highQualityCrop = fields.parallelStream().mapToLong(it -> it.getHighQualityCrop().longValue()).average().getAsDouble();
        Double lowQualityCrop = fields.parallelStream().mapToLong(it -> it.getLowQualityCrop().longValue()).average().getAsDouble();
        Double inFertileLand = fields.parallelStream().mapToLong(it -> it.getInFertileLand().longValue()).average().getAsDouble();
        Double water = fields.parallelStream().mapToLong(it -> it.getWater().longValue()).average().getAsDouble();
        Double windSpeed = fields.parallelStream().mapToLong(it -> it.getWindSpeed().longValue()).average().getAsDouble();
        Double other = fields.parallelStream().mapToLong(it -> it.getOther().longValue()).average().getAsDouble();
        Map<String, Double> map = new HashMap<>();
        map.put("cultivatedLand", cultivatedLand);
        map.put("damageArea", damageArea);
        map.put("highQualityCrop", highQualityCrop);
        map.put("lowQualityCrop", lowQualityCrop);
        map.put("inFertileLand", inFertileLand);
        map.put("water", water);
        map.put("windSpeed", windSpeed);
        map.put("other", other);
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

    public ResponseDto saveField(String inspectionId, FieldData fieldData) {
        Optional<Inspection> optionalInspection = inspectionRepository.findById(inspectionId);
        if (optionalInspection.isPresent()) {
            Inspection inspection = optionalInspection.get();
            inspection.getFieldDataList().add(fieldDataRepository.save(fieldData));
            inspectionRepository.save(inspection);
        }
        return ResponseDto.builder().status(true).message("FieldData is Created Successfully").build();
    }

    @Cacheable(value = "inspections", key = "#id")
    public ResponseDto get(String id) {
        Optional<Inspection> optional = inspectionRepository.findById(id);
        if (optional.isPresent()) {
            Inspection inspection = optional.get();
            return ResponseDto.builder().status(true).data(inspection).build();
        }
        return ResponseDto.builder().status(false).message("Inspection is not found in DB").build();
    }

    @Cacheable(value = "inspectionsFindByCustomerId", key = "#customerId")
    public ResponseDto findByCustomerId(String customerId) {
        List<Inspection> inspectionList = inspectionRepository.findAllByCustomerId(customerId);
        if (!CollectionUtils.isEmpty(inspectionList)) {

            return ResponseDto.builder().status(true).data(inspectionList).build();
        }
        return ResponseDto.builder().status(false).message("Customer is not found in DB").build();
    }

    //    @Cacheable(value = "findByCustomerIdAndPolicyId", key = "#customerId.concat(policyId)")
    public ResponseDto findByCustomerIdAndPropertyId(String customerId, String policyId) {
        List<Inspection> inspectionList = null;
        return ResponseDto.builder().status(true).data(inspectionList).build();
    }

    public ResponseDto findAll() {
        return ResponseDto.builder().status(true).data(inspectionRepository.findAll()).build();
    }

    public ResponseDto delete(String id) {
        inspectionRepository.deleteById(id);
        return ResponseDto.builder().status(true).message("Inspection is deleted successfully").build();
    }

    public ResponseDto delete() {
        inspectionRepository.deleteAll();
        return ResponseDto.builder().status(true).message("All Inspections are deleted successfully").build();
    }

}
