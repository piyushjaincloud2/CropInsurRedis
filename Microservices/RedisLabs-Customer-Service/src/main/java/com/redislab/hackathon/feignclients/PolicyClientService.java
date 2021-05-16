package com.redislab.hackathon.feignclients;

import org.springframework.cloud.openfeign.FeignClient;

@FeignClient(name = "Policy", url = "${feign.policy.url}")
public interface PolicyClientService {
}
