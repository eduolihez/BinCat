<div align="center"> <h1> <img src="https://repository-images.githubusercontent.com/420671000/5d7994a7-0991-4257-a52b-b993e9443992" width="80px"><br/>BinCat Token System</h1> </div> <p align="center"> <a href="http://delaas.xyz" target="_blank"><img alt="" src="https://img.shields.io/badge/Website-EA4C89?style=normal&logo=dribbble&logoColor=white" style="vertical-align:center" /></a> <a href="@Hipotesi_dev" target="_blank"><img alt="" src="https://img.shields.io/badge/Twitter-1DA1F2?style=normal&logo=twitter&logoColor=white" style="vertical-align:center" /></a> <a href="@_eduoliihezz" target="_blank"><img alt="" src="https://img.shields.io/badge/Instagram-E4405F?style=normal&logo=instagram&logoColor=white" style="vertical-align:center" /></a> <a href="}" target="_blank"><img alt="" src="https://img.shields.io/badge/LinkedIn-0077B5?style=normal&logo=linkedin&logoColor=white" style="vertical-align:center" /></a> </p>

# Description

BinCat is an innovative login system that enhances the security of registered accounts. This project is inspired by a conventional token system.

# Features

BinCat generates a 10-digit ID _(1234567890)_. Each user's ID is encrypted in Base64, with seven random uppercase and lowercase letters and numbers separated by a dot. Another dot separates it from the current date of token creation, which is also encrypted in Base64. The resulting format looks like this:

`MTIzNDU2Nzg5MA ==. ADJrNnB.Jsw97Jhb29`

# Screenshots

<img src="https://github.com/Hipotesi-Dev/BinCat/blob/main/BinCat%20Demo.PNG">

# Tech Used

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Notion](https://img.shields.io/badge/Notion-%23000000.svg?style=for-the-badge&logo=notion&logoColor=white)

## 🛠 Installation

Windows, macOS, and Linux:

1.  Download the program:

```sh
https://github.com/titodelas/BinCat.git
```

2.  Install requirements:

```sh
pip install colorama
```

3.  Execute BinCat Token Generator:

```sh
python BinCat.py
```

## Future To-Do ✅

- **Token Verification:** Implement a token verification system where you can validate the authenticity and integrity of a token. This can involve verifying the signature, checking the token expiration date, and ensuring it hasn't been tampered with.
- **Token Revocation:** Add functionality to revoke or invalidate tokens if needed. This could be useful in scenarios where a token needs to be invalidated due to security breaches, user logout, or account deactivation.
- **Token Refreshing:** Enable token refreshing to improve security and user experience. When a token expires, users can obtain a new token using a refresh token, eliminating the need to log in again with their credentials.
- **Multi-factor Authentication (MFA):** Enhance security by incorporating MFA into the token generation process. Users can be required to provide an additional factor such as a one-time password (OTP) or biometric verification to generate or access tokens.
- **Role-based Access Control (RBAC):** Integrate RBAC to manage user permissions and access levels using tokens. Tokens can contain information about the user's role, which can then be used to determine what resources they can access within an application or system.
- **Token Expiration and Revocation Management:** Develop a mechanism to handle token expiration and revocation efficiently. This can include automatic token expiration, token blacklist/whitelist management, and efficient token storage and retrieval.
- **Token Auditing and Logging:** Implement logging and auditing mechanisms to track token usage, including token creation, validation, and revocation. This can assist with security monitoring, troubleshooting, and compliance requirements.
- **Token-Based Authentication for APIs:** Extend your project to support token-based authentication for APIs. This would allow other systems or applications to authenticate and authorize access by validating tokens issued by your system.
- **Token Encryption Algorithms:** Explore different encryption algorithms or standards (such as JWT - JSON Web Tokens) to encode and sign your tokens. This can offer increased security and interoperability with other systems.
- **Web Interface and Administration:** Build a user-friendly web interface for token management, administration, and configuration. This can include features like token generation, revocation, expiration setting, and user management.

## 🧬Version Notes

BinCat updates and notes can be found in the dropdown below ⬇

<details open> <summary>📑 Version history</summary> <br>

- 1.6.3
  - UPDATE: The readme.md has been updated for clarity.
- 1.6.2
  - ADD: Added templates for issues.
  - ADD: Created security.md.
  - TESTED: QR code generator with the token.
- 1.6.1
  - TRANSLATION: BinCat is now available in Spanish and English (I'm a Spanish developer, so the variables and other things can be in Spanish ^^).
  - REPLACE: The previous name "Gato" for BinCat token has been deleted. All variables, names, etc. have been replaced with "Token".
- 1.6.0
  - UPDATE: BinCat now saves the token in a QR code (.png) in the directory where the program is running.
- 1.5.2
  - CHANGE: Documentation update (the code of the program remains the same).
- 1.5.1
  - CODE COMPILED: Made some minor modifications to the code, now it can be compiled without errors.
- 1.5.0
  - CLEAN CODE: Removed unnecessary code from BinCat.
- 0.1.0 - 1.5.0
  - Building BinCat System.
  - Improving the code.
- 0.0.1
  - Working on BinCat.

</details>

## ✍ Credits

Distributed under the Apache2.0 License. See `LICENSE` for more information.

[BinCat Open-Source Project](https://github.com/Hipotesi-Dev/BinCat)

⌨ with ❤ by Edu Olivares

## 🤝 Contributing

1.  Fork it ([https://github.com/titodelas/BinCat/fork](https://github.com/titodelas/BinCat/fork))
2.  Create your feature branch (`git checkout -b feature/fooBar`)
3.  Commit your changes (`git commit -am 'Add some fooBar'`)
4.  Push to the branch (`git push origin feature/fooBar`)
5.  Create a new Pull Request.
