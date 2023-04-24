package io.github.nandandesai.pico.controllers;

import io.github.nandandesai.pico.dto.Photo;
import io.github.nandandesai.pico.dto.UserDto;
import io.github.nandandesai.pico.dto.requests.*;
import io.github.nandandesai.pico.dto.responses.Response;
import io.github.nandandesai.pico.dto.responses.ResponseType;
import io.github.nandandesai.pico.exceptions.*;
import io.github.nandandesai.pico.services.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.List;

@RestController
@RequestMapping("/base")
public class UserController {

    private Logger logger = LoggerFactory.getLogger(UserController.class);

    @Autowired
    private UserService userService;

    @GetMapping("/users")
    public Response<List<UserDto>> getAll() {
        List<UserDto> userList = userService.getAllUsers();
        Response<List<UserDto>> response = new Response<>();
        response.setPayload(userList);
        response.setType(ResponseType.SUCCESS);
        return response;
    }

    @GetMapping("/users/{id}")
    public Response<UserDto> getUser(@PathVariable("id") Integer id) throws ResourceNotFoundException {
        Response<UserDto> response = new Response<>();
        response.setPayload(userService.getUser(id));
        response.setType(ResponseType.SUCCESS);
        return response;
    }

    @PostMapping("/signup")
    public Response<String> signUp(@Valid @RequestBody UserSignUpRequest userSignUpRequest) throws InternalServerException, DuplicateEntityException {
        String token = userService.addUser(userSignUpRequest);
        return new Response<String>().setPayload(token)
                .setType(ResponseType.SUCCESS);
    }

    @PostMapping("/login")
    public Response<String> login(@Valid @RequestBody UserLoginRequest userLoginRequest) throws LoginFailedException {
        String token = userService.login(userLoginRequest);
        return new Response<String>().setPayload(token)
                .setType(ResponseType.SUCCESS);
    }

    @PatchMapping("/users/pass")
    public Response<String> updatePassword(@Valid @RequestBody UpdateUserPasswordRequest userPasswordRequest) throws ResourceNotFoundException, ValidationException {
        userService.updatePassword(userPasswordRequest);
        return new Response<String>().setPayload("Password successfully updated.")
                .setType(ResponseType.SUCCESS);
    }

    @PatchMapping("/users/role")
    public Response<String> updateRole(@Valid @RequestBody UpdateUserRoleRequest userRoleRequest) throws ResourceNotFoundException, ValidationException {
        userService.updateRole(userRoleRequest);
        return new Response<String>().setPayload("Role successfully updated.")
                .setType(ResponseType.SUCCESS);
    }

    @PostMapping("/users/photo")
    public Response<String> photoUpload(@Valid @ModelAttribute AddUserPhotoRequest addUserPhotoRequest) throws InternalServerException, ResourceNotFoundException {
        userService.saveUserPhoto(addUserPhotoRequest);
        return new Response<String>().setPayload("Successfully uploaded")
                .setType(ResponseType.SUCCESS);
    }

    @GetMapping("/users/photo/{id}")
    public ResponseEntity<byte[]> getPhoto(@PathVariable("id") Integer id) throws ResourceNotFoundException, InternalServerException {
        Photo photo = userService.getUserPhoto(id);
        byte[] photoBytes = photo.getPhotoBytes();
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.parseMediaType(photo.getMimeType()));
        return new ResponseEntity<>(photoBytes, headers, HttpStatus.OK);
    }
}
