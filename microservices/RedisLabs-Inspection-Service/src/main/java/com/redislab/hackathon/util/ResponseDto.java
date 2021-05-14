package com.redislab.hackathon.util;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Builder;
import lombok.Data;
import org.hibernate.annotations.Proxy;

import java.io.Serializable;

@Data
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
@Proxy(lazy = false)
public class ResponseDto implements Serializable {
    private static final long serialVersionUID = 1L;
    private boolean status;
    private String message;
    private Object data;
}
