package com.redislab.hackathon.controller;

import com.redislab.hackathon.domain.Inspection;
import com.redislab.hackathon.service.InspectionService;
import com.redislab.hackathon.util.ResponseDto;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("inspection")
public class InspectionController {
    @Autowired
    private InspectionService inspectionService;

    @PostMapping("/save")
    public ResponseDto save(@RequestBody Inspection inspection) {
        return inspectionService.save(inspection);
    }

    @GetMapping("/findByCustomerId/{id}")
    public ResponseDto findByCustomerId(@PathVariable String id) {
        return inspectionService.findByCustomerId(id);
    }

    @GetMapping("/findByCustomerIdAndPropertyId")
    public ResponseDto findByCustomerIdAndPolicyId(@RequestParam String customerId, @RequestParam String policyId) {
        return inspectionService.findByCustomerIdAndPropertyId(customerId, policyId);
    }

    @GetMapping("/get/{id}")
    public ResponseDto get(@PathVariable String id) {
        return inspectionService.get(id);
    }

    @RequestMapping(value = "/delete/{id}", method = {RequestMethod.DELETE, RequestMethod.GET})
    public ResponseDto delete(@PathVariable String id) {
        return inspectionService.delete(id);
    }

    @RequestMapping(value = "/delete", method = {RequestMethod.DELETE, RequestMethod.GET})
    public ResponseDto delete() {
        return inspectionService.delete();
    }

    @GetMapping("/get")
    public ResponseDto findAll() {
        return inspectionService.findAll();
    }
}
