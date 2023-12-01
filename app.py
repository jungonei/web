import streamlit as st
from sqlalchemy import text

list_jenis_kelamin = ['', 'Perempuan', 'Laki-Laki']

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://helvytianarn:5uEaoKh2VFGP@ep-shy-frog-96637425.us-east-2.aws.neon.tech/web")
with conn.session as session:
    query = text('CREATE TABLE IF NOT EXISTS MAHASISWA (id serial, nama varchar, nrp int, jenis_kelamin varchar, \
                                                       tempat_lahir varchar, tanggal_lahir date, asal varchar, alamat_domisili varchar);')
    session.execute(query)

st.header('DATA MAHASISWA')
page = st.sidebar.selectbox("Pilih Menu", ["View Data","Edit Data"])

if page == "View Data":
    data = conn.query('SELECT * FROM MAHASISWA ORDER By id;', ttl="0").set_index('id')
    st.dataframe(data)

if page == "Edit Data":
    if st.button('Tambah Data'):
        with conn.session as session:
            query = text('INSERT INTO MAHASISWA (nama, nrp, jenis_kelamin, tempat_lahir, tanggal_lahir, asal, alamat_domisili) \
                          VALUES (:1, :2, :3, :4, :5, :6, :7);')
            session.execute(query, {'1':'', '2':'', '3':'', '4':'', '5':None, '6':'', '7':''})
            session.commit()

    data = conn.query('SELECT * FROM MAHASISWA ORDER By id;', ttl="0")
    for _, result in data.iterrows():        
        id = result['id']
        nama_lama = result["nama"]
        nrp_lama = result["nrp"]
        jenis_kelamin_lama = result["jenis_kelamin"]
        tempat_lahir_lama = result["tempat_lahir"]
        tanggal_lahir_lama = result["tanggal_lahir"]
        asal_lama = result["asal"]
        alamat_domisili_lama = result["alamat_domisili"]

        with st.expander(f'a.n. {nama_lama}'):
            with st.form(f'data-{id}'):
                nama_baru = st.text_input("nama", nama_lama)
                nrp_baru = st.text_input("nrp", nrp_lama)
                jenis_kelamin_baru = st.selectbox("jenis_kelamin", list_jenis_kelamin, list_jenis_kelamin.index(jenis_kelamin_lama))
                tempat_lahir_baru = st.text_input("tempat_lahir", tempat_lahir_lama)
                tanggal_lahir_baru = st.date_input("tanggal_lahir", tanggal_lahir_lama)
                asal_baru = st.text_input("asal", asal_lama)
                alamat_domisili_baru = st.text_input("alamat_domisili", alamat_domisili_lama)
                
                col1, col2 = st.columns([1, 6])

                with col1:
                    if st.form_submit_button('UPDATE'):
                        with conn.session as session:
                            query = text('UPDATE MAHASISWA \
                                          SET nama=:1, nrp=:2, jenis_kelamin=:3, tempat_lahir=:4, \
                                          tanggal_lahir=:5, asal=:6, alamat_domisili=:7 \
                                          WHERE id=:8;')
                            session.execute(query, {'1':nama_baru, '2':nrp_baru, '3':jenis_kelamin_baru, '4':tempat_lahir_baru, 
                                                    '5':tanggal_lahir_baru, '6':asal_baru, '7':alamat_domisili_baru, '8':id})
                            session.commit()
                            st.experimental_rerun()
                
                with col2:
                    if st.form_submit_button('DELETE'):
                        query = text(f'DELETE FROM MAHASISWA WHERE id=:1;')
                        session.execute(query, {'1':id})
                        session.commit()
                        st.experimental_rerun()