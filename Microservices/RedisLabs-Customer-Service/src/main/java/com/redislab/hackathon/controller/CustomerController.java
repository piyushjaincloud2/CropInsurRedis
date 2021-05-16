package com.redislab.hackathon.controller;

import com.redislab.hackathon.domain.Customer;
import com.redislab.hackathon.service.CustomerService;
import com.redislab.hackathon.util.ResponseDto;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("customer")
public class CustomerController {
    @Autowired
    private CustomerService customerService;

    @PostMapping("/save")
    public ResponseDto save(@RequestBody Customer customer) {
        return customerService.save(customer);
    }


    @GetMapping("/get/{id}")
    public ResponseDto get(@PathVariable String id) {
        return customerService.get(id);
    }

    @RequestMapping(value = "/delete/{id}", method = {RequestMethod.DELETE, RequestMethod.GET})
    public ResponseDto delete(@PathVariable String id) {
        return customerService.delete(id);
    }

    @RequestMapping(value = "/delete", method = {RequestMethod.DELETE, RequestMethod.GET})
    public ResponseDto delete() {
        return customerService.delete();
    }

    @GetMapping("/get")
    public ResponseDto findAll() {
        return customerService.findAll();
    }
}
