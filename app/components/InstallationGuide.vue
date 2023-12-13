<template>
    <div id="installation-comp" class="main-comp">
        <div class="setting-title">
            <span>Installation Guide</span>
            <div>
                <!--to: /dashboard/installation-guide/theme -->
                <div class="btn primary">Go to Themes
                    Customization</div>
            </div>
        </div>
        <div class="ig-body">
            <div class="ig-box">
                <span class="ig-title">CONGRATULATION! YOU HAVE CREATED WIDGET SUCCESSFULLY!</span>
                <span class="ig-des">Now please follow these steps below to display it on your product pages</span>
                <ol class="ig-text" >
                    <li>Lorem ipsum is placeholder text commonly used in the graphic, print</li>
                    <li>and publishing industries for previewing layouts and visual mockups.</li>
                    <li>Lorem ipsum is placeholder text commonly used in the graphic, print, and publishing
                        industries for previewing layouts and visual mockups.</li>
                </ol>
            </div>
            <div>
                <iframe width="670" height="258" src="https://www.youtube.com/embed/JfLBwfQiAao?si=ffxI5p8-stqSjarR"
                    title="YouTube video player" frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                    allowfullscreen></iframe>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            videoUrl: 'https://www.youtube.com/watch?v=7wLhd571ZI0'
        }
    },
}
</script>

<style scoped>
.ig-body{
    display: flex; 
    width: 100%;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 40px;
    flex-shrink: 0;
    border-radius: 6px;
    border: 1px solid #E2E2E2;
    background: #FFF;
    padding-top: 72px;
    padding-bottom: 72px;
}

.ig-box{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center; 
}

.ig-title{
    color: #000;
    text-align: center;
    font-family: Inter;
    font-size: 20px;
    font-style: normal;
    font-weight: 700;
    line-height: 22px;
}

.ig-des{
    color: #000;
    font-family: Inter;
    font-size: 14px;
    font-style: normal;
    font-weight: 700;
    line-height: 22px;
    margin-top: 24px;
}

.ig-text{
    width: 752px;
    color: #000;
    font-family: Inter;
    font-size: 14px;
    font-style: normal;
    font-weight: 400;
    line-height: 22px; /* 157.143% */
    margin-top: 36px;
}

</style>