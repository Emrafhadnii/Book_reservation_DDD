from src.auth.domain.commands import LoginCommand, VerifyCommand
from fastapi import HTTPException
from src.auth.services.otp_service import otp_generator, otp_validator
from src.auth.services.JWT import JWTService
from src.users.domain.events import UserEvents
from src.users.domain.entities.Users import User
from uuid import uuid4


class Auth_Command_Handler:

    @staticmethod
    async def login(form_data: LoginCommand, uow, redis):
        user_uow = uow.user
        user = await user_uow.get_by_phone(form_data.phone)

        if not user or (str(form_data.password) != str(user.password)):
            raise HTTPException(status_code=400,detail="Incorrect email or password")

        user_identifier = str(uuid4())
        await redis.setex(
            name=f"login_identifier:{user_identifier}",
            time=120,
            value=str(user.phone)
            )

        otp_code = await otp_generator(user.phone, redis)

        await redis.delete(f"login_{120}:{form_data.phone}")
        await redis.delete(f"login_{3600}:{form_data.phone}")
        
        return {
            "message": "otp sent",
            "user_identifier": user_identifier,
            "otp_code": otp_code
            }
    
    @staticmethod
    async def verification(verifyotp: VerifyCommand, redis,
                           uow, bus):
        user_phone = await redis.get(f"login_identifier:{verifyotp.user_identifier}")
        if not user_phone:
            raise HTTPException(400, "identifier expired or invalid")

        if not await otp_validator(user_identifier=user_phone, otp=verifyotp.otp_code, redis=redis):
            raise HTTPException(400, "Invalid OTP")
        
        await uow.commit()

        user = await uow.user.get_by_phone_all(user_phone)

        await UserEvents.usercreated_event(bus,user.model_dump_json())
        

        return {
        "access_token": JWTService.create_access_token({
        "sub": str(user.id),"phone": user.phone,"role": user.user_role}),        
        "refresh_token": JWTService.create_refresh_token({
            "sub": str(user.id)}),"token_type": "bearer"
            }
    
    @staticmethod
    async def sign_up(model, repos, redis):
        try:
            user_repo = repos.user
            
            user = User(username=model.username,first_name=model.first_name,
                        last_name=model.last_name,
                        user_password=model.user_password,
                        email=model.email,
                        phone=model.phone,user_role=model.user_role)
            
            await user_repo.add(user)

            user_identifier = str(uuid4())
            await redis.setex(
            name=f"login_identifier:{user_identifier}",
            time=120,
            value=str(user.phone)
            )

            otp_code = await otp_generator(user_identifier=user.phone,redis=redis)

            return {
                "messgae": "account created successfully",
                "user_identifier": user_identifier,
                "otp_code": otp_code
            }

        except Exception as e:
            raise HTTPException(400,detail=[str(e)])
