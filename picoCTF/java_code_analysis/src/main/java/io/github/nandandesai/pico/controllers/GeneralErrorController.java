package io.github.nandandesai.pico.controllers;

import org.springframework.boot.web.servlet.error.ErrorController;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
public class GeneralErrorController  implements ErrorController {
    @RequestMapping(value = "/error")
    public String handleError() {
        return "/error.html";
    }

    @Override
    public String getErrorPath() {
        return "/error";
    }
}
