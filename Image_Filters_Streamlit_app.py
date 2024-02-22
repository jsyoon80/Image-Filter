import io
import base64
import cv2
from PIL import Image
from filters import *
from thresh import *

# 로고 준비해서 넣기
col1, col2, col3 = st.columns(3)
with col1:
    st.image('AiProVision_Disit_Logo.png')  # 'image_path'를 실제 이미지 경로로 바꿔주세요.
with col2:
    st.write('')
with col3:
    st.write('')

# Set title.
st.title('Artistic 이미지 필터 프로그램')


# Generating a link to download a particular image file.
def get_image_download_link(img, filename, text):
    buffered = io.BytesIO()
    img.save(buffered, format = 'JPEG')
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/txt;base64,{img_str}" download="{filename}">{text}</a>'
    return href



# Upload image.
uploaded_file = st.file_uploader('이미지 파일을 선택하세요:', type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Convert the file to an opencv image.
    raw_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(raw_bytes, cv2.IMREAD_COLOR)
    input_col, output_col = st.columns(2)
    with input_col:
        st.header('Original')
        # Display uploaded image.
        st.image(img, channels='BGR', use_column_width=True)

    st.header('Filter Examples:')
    # Display a selection box for choosing the filter to apply.
    option = st.selectbox('아래릐 필터 종류를 하나 선택해 주세요.:',
                          ( 'None',
                            'Black and White',
                            'Sepia / Vintage',
                            'Vignette Effect',
                            'Pencil Sketch',
                            'Image Thresh',
                         ))

    # Define columns for thumbnail images.
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.caption('Black and White')
        st.image('filter_bw.jpg')
    with col2:
        st.caption('Sepia / Vintage')
        st.image('filter_sepia.jpg')
    with col3:
        st.caption('Vignette Effect')
        st.image('filter_vignette.jpg')
    with col4:
        st.caption('Pencil Sketch')
        st.image('filter_pencil_sketch.jpg')
    with col5:
        st.caption('Image Thresh')
        st.image('kitten.jpg')

    # Flag for showing output image.
    output_flag = 1
    # Colorspace of output image.
    color = 'BGR'

     # Generate filtered image based on the selected option.
    if option == 'None':
        # Don't show output image.
        output_flag = 0
    elif option == 'Black and White':
        output = bw_filter(img)
        color = 'GRAY'
    elif option == 'Sepia / Vintage':
        output = sepia(img)
    elif option == 'Vignette Effect':
        level = st.slider('level', 0, 5, 2)
        output = vignette(img, level)
    elif option == 'Pencil Sketch':
        ksize = st.slider('Blur kernel size', 1, 11, 5, step=2)
        output = pencil_sketch(img, ksize)
        color = 'GRAY'
    elif option == 'Image Thresh':
        ksize = st.slider('Blur kernel size', 1, 255, 100, step=2)
        output = image_thresh(img, ksize)
        color = 'GRAY'

    with output_col:
        if output_flag == 1:
            st.header('Output')
            st.image(output, channels=color)
            # fromarray convert cv2 image into PIL format for saving it using download link.
            if color == 'BGR':
                result = Image.fromarray(output[:,:,::-1])
            else:
                result = Image.fromarray(output)
            # Display link.
            st.markdown(get_image_download_link(result,'output.png','Download '+'Output'),
                        unsafe_allow_html=True)
    