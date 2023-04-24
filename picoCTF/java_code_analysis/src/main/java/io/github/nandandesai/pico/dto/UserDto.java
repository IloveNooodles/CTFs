package io.github.nandandesai.pico.dto;

import io.github.nandandesai.pico.models.User;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import lombok.experimental.Accessors;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Getter
@Setter
@Accessors(chain = true)
@NoArgsConstructor
@ToString
public class UserDto {
    private Integer id;
    private String email;
    private String fullName;
    private LocalDateTime lastLogin;
    private String role;

    public static UserDto getUserDtoFromUser(User user) {
        return new UserDto()
                .setId(user.getId())
                .setEmail(user.getEmail())
                .setFullName(user.getFullName())
                .setLastLogin(user.getLastLogin())
                .setRole(user.getRole().getName());
    }

    public static List<UserDto> getUserDtoListFromUsers(List<User> userList) {
        List<UserDto> userDtoList = new ArrayList<>();
        for (User user : userList) {
            userDtoList.add(getUserDtoFromUser(user));
        }
        return userDtoList;
    }
}
