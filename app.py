import streamlit as st
from auth_service import send_flash_call
from bitrix_integration import get_active_deals, close_deal
from exolve_voice import initiate_masked_call


st.set_page_config(page_title="Кабинет курьера", page_icon="🚚")
st.title("🚚 Кабинет водителя")


if "auth" not in st.session_state:
    st.session_state.auth = False


if not st.session_state.auth:
    phone = st.text_input("Ваш телефон", placeholder="79990000000")

    if st.button("Получить код доступа"):
        with st.spinner("Звоним..."):
            code = send_flash_call(phone)
            if code:
                st.session_state.verification = code
                st.success("Ждите звонка-сброса. Введите последние 4 цифры.")
            else:
                st.error("Ошибка дозвона")

    user_code = st.text_input("Код из звонка")
    if st.button("Войти"):
        if user_code == st.session_state.get("verification"):
            st.session_state.auth = True
            st.session_state.phone = phone
            st.rerun()
        else:
            st.error("Неверный код")
else:
    with st.spinner("Загрузка заказов..."):
        deals = get_active_deals(st.session_state.phone)

    if not deals:
        st.info("Нет активных заказов. Отдыхайте!")

    for deal in deals:
        with st.container(border=True):
            st.subheader(f"📦 Заказ #{deal['id']}")
            st.write(f"🏠 **Адрес:** {deal['address']}")
            st.write(f"📝 **Детали:** {deal['title']}")

            c1, c2 = st.columns(2)

            if c1.button("📞 Связаться", key=f"call_{deal['id']}"):
                initiate_masked_call(
                    master_phone=st.session_state.phone,
                    client_phone=deal["client_phone_hidden"],
                )
                st.toast("Соединяем... Ждите входящий.")

            if c2.button("✅ Выполнил", key=f"done_{deal['id']}"):
                close_deal(deal["id"])
                st.success("Заказ закрыт!")
                st.rerun()
