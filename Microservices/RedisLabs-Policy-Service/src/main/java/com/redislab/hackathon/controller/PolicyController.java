package com.redislab.hackathon.controller;

import com.redislab.hackathon.domain.Claim;
import com.redislab.hackathon.domain.Policy;
import com.redislab.hackathon.service.PolicyService;
import com.redislab.hackathon.util.ResponseDto;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("policy")
public class PolicyController {

    @Autowired
    private PolicyService policyService;

    @PostMapping("/save")
    public ResponseDto save(@RequestBody Policy policy) {
        return policyService.save(policy);
    }

    @PostMapping("/claim")
    public ResponseDto save(@RequestBody Claim claim) {
        return policyService.claim(claim);
    }
    @GetMapping("/get/{id}")
    public ResponseDto get(@PathVariable String id) {
        return policyService.get(id);
    }

    @RequestMapping(value = "/delete/{id}", method = {RequestMethod.DELETE, RequestMethod.GET})
    public ResponseDto delete(@PathVariable String id) {
        return policyService.delete(id);
    }

    @GetMapping(value = "/delete")
    public ResponseDto deleteAll() {
        return policyService.delete();
    }
}
