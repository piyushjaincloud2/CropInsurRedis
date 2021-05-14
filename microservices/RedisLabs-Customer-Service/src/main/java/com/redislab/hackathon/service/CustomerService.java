package com.redislab.hackathon.service;

import com.redislab.hackathon.domain.Customer;
import com.redislab.hackathon.domain.Property;
import com.redislab.hackathon.repository.CustomerRepository;
import com.redislab.hackathon.util.ResponseDto;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class CustomerService {
    @Autowired
    private CustomerRepository customerRepository;

    public ResponseDto save(Customer customer) {
        Customer dbCustomer = customerRepository.save(customer);
        Map<String, Object> response = new HashMap<>();
        response.put("customerId", dbCustomer.getId());
        response.put("properties", dbCustomer.getProperties().stream().map(Property::getId).collect(Collectors.toList()));
        return ResponseDto.builder().status(true).data(response).message("Customer is Saved Successfully").build();
    }

    public ResponseDto get(String id) {
        Optional<Customer> optional = customerRepository.findById(id);
        if (optional.isPresent()) {
            Customer customer = optional.get();
            return ResponseDto.builder().status(true).data(customer).build();
        }
        return ResponseDto.builder().status(false).message("Customer is not found in DB").build();
    }

    public ResponseDto delete(String id) {
        customerRepository.deleteById(id);
        return ResponseDto.builder().status(true).message("Customer is deleted successfully").build();
    }

    public ResponseDto delete() {
        customerRepository.deleteAll();
        return ResponseDto.builder().status(true).message("Customers are deleted successfully").build();
    }

    public ResponseDto findAll() {
        List<Customer> customerList = customerRepository.findAll();
        return ResponseDto.builder().status(true).data(customerList).build();
    }
}
