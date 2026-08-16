<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'


const scrollProgress = ref(0)

const handleScroll = () => {
  const scrollTop = window.scrollY

  const maxScroll =
    document.documentElement.scrollHeight - window.innerHeight

  scrollProgress.value =
    maxScroll > 0
      ? Math.min(scrollTop / maxScroll, 1)
      : 0
}

const mouseX = ref(0)
const mouseY = ref(0)

const handleMouseMove = (event) => {
  mouseX.value = event.clientX
  mouseY.value = event.clientY
}


onMounted(() => {
  handleScroll()

  window.addEventListener('scroll', handleScroll, {
    passive: true
  })

  window.addEventListener('mousemove', handleMouseMove, {
    passive: true
  })
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('mousemove', handleMouseMove)
})




const glassScale = computed(() => {
  const progress = Math.min(
    scrollProgress.value / 0.78,
    1
  )

  return 1 + progress * 2
})
const magglassScale = computed(() => {
  const progress = Math.min(
    scrollProgress.value / 0.78,
    1
  )

  return 1 + progress * 4
})


/*glass shatter*/

const shatter = computed(() => {
  if (scrollProgress.value < 0.78) {
    return 0
  }

  return Math.min(
    (scrollProgress.value - 0.78) / 0.22,
    1
  )
})

const glassOpacity = computed(() => {
  return 1 - shatter.value
})

const shardOpacity = computed(() => {
  return shatter.value
})

const distance = computed(() => {
  return shatter.value * 180
})


/*cube*/

const cubeScale = computed(() => {

  if (scrollProgress.value < 0.30) {
    return 0
  }

  const progress = Math.min(
    (scrollProgress.value - 0.30) / 0.52,
    1
  )

  return 1 + progress * 3
})


const cubeOpacity = computed(() => {

  if (scrollProgress.value < 0.30) {
    return 0
  }

  if (scrollProgress.value >= 0.82) {
    return 0
  }

  return 1
})



const cubeShatter = computed(() => {

  if (scrollProgress.value < 0.82) {
    return 0
  }

  return Math.min(
    (scrollProgress.value - 0.82) / 0.18,
    1
  )
})



const cubeDistance = computed(() => {
  return cubeShatter.value * 280
})



const paperOpacity = computed(() => {
  return cubeShatter.value
})



const documentPieces = [
  {
    x: -1.5,
    y: -1.2,
    rotate: -35,
    width: 150,
    height: 200,
    title: 'REPORT'
  },

  {
    x: 0,
    y: -1.6,
    rotate: 20,
    width: 155,
    height: 215,
    title: 'DATA'
  },

  {
    x: 1.5,
    y: -1.1,
    rotate: 40,
    width: 150,
    height: 200,
    title: 'MAP'
  },

  {
    x: -1.8,
    y: 0,
    rotate: -25,
    width: 145,
    height: 190,
    title: 'AREA'
  },

  {
    x: 1.8,
    y: 0,
    rotate: 30,
    width: 145,
    height: 195,
    title: 'INFO'
  },

  {
    x: -1.4,
    y: 1.4,
    rotate: 35,
    width: 145,
    height: 190,
    title: 'FILE'
  },

  {
    x: 0,
    y: 1.7,
    rotate: -20,
    width: 150,
    height: 205,
    title: 'SUGBO'
  },

  {
    x: 1.4,
    y: 1.3,
    rotate: 45,
    width: 145,
    height: 190,
    title: 'DOC'
  }
]



const getPieceTransform = (piece) => {

  const d = cubeDistance.value

  return `
    translate(
      ${piece.x * d}px,
      ${piece.y * d}px
    )
    rotate(${cubeShatter.value * piece.rotate}deg)
    scale(${0.65 + cubeShatter.value * 0.35})
  `
}


const backgroundStyle = computed(() => {

  const progress = scrollProgress.value

  return {
    transform: `
      translate(
        ${Math.sin(progress * Math.PI * 4) * 40}px,
        ${Math.cos(progress * Math.PI * 3) * 30}px
      )
      scale(${1 + progress * 0.15})
      rotate(${progress * 8}deg)
    `
  }
})

</script>


<template>
  <main class="relative min-h-[300vh] overflow-hidden  text-white">
    <div class="pointer-events-none fixed z-50 size-[300px] -translate-x-1/2 -translate-y-1/2 rounded-full blur-3xl"
      :style="{
        left: `${mouseX}px`,
        top: `${mouseY}px`
        }"
      >
    </div>


   <!--PH-->

    <div class="pointer-events-none fixed inset-0 z-0 flex items-center justify-center overflow-hidden">
      <img src="/ph.svg" class="w-[80%] max-w-5xl opacity-10 transition-transform duration-700 ease-out" 
        :style="backgroundStyle"
      />
    </div>


  <!--cube-->
    <div class="pointer-events-none fixed inset-0 z-5 flex items-center justify-center"
      :style="{
        opacity: cubeOpacity
      }"
    >
      <!-- Cube container -->
      <div class="relative size-24 [perspective:800px]"
        :style="{
          transform: `scale(${cubeScale})`
        }"
      >
        <!-- Actual cube -->
        <div class="relative size-24 [transform-style:preserve-3d] animate-[cube-rotate_8s_linear_infinite]">

          <!-- FRONT /DATA-->
          <div class="cube-face absolute inset-0 flex size-24 items-center justify-center rounded-lg bg-sky-300/80 text-sm font-bold text-slate-900 shadow-[0_0_40px_rgba(56,189,248,0.5)] [transform:translateZ(48px)]">
            DATA
          </div>

          <!-- BACK/info -->
          <div class="cube-face absolute inset-0 flex size-24 items-center justify-center rounded-lg bg-sky-300/80 text-sm font-bold text-slate-900 [transform:rotateY(180deg)_translateZ(48px)]">
            INFO
          </div>

          <!-- RIGHT/ -->
          <div
            class="cube-face absolute inset-0 flex size-24 items-center justify-center rounded-lg bg-sky-300/80 text-sm font-bold text-slate-900 [transform:rotateY(90deg)_translateZ(48px)]">
            MAP
          </div>

          <!-- LEFt/area -->
          <div class = "cube-face absolute inset-0 flex size-24 items-center justify-center rounded-lg bg-sky-300/80 text-sm font-bold text-slate-900 [transform:rotateY(-90deg)_translateZ(48px)]">
            AREA
          </div>

          <!-- TOP -->
          <div class="cube-face absolute inset-0 flex size-24 items-center justify-center rounded-lg bg-sky-300/80 text-sm font-bold text-slate-900 [transform:rotateX(90deg)_translateZ(48px)]">
            SEARCH
          </div>


          <!-- BOTTOM/ data -->
          <div class="cube-face absolute inset-0 flex size-24 items-center justify-center rounded-lg bg-sky-300/80 text-sm font-bold text-slate-900 [transform:rotateX(-90deg)_translateZ(48px)]">
            DATA
          </div>

        </div>

      </div>

    </div>


    <!-- docs flying-->

    <div class="pointer-events-none fixed inset-0 z-6"
      :style="{
        opacity: paperOpacity
      }"
    >

      <div class="relative h-full w-full">
        <div
          v-for="(piece, index) in documentPieces"
          :key="index"
          class="document-piece absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2"
          :style="{
            width: `${piece.width}px`,
            height: `${piece.height}px`,
            transform: getPieceTransform(piece)
          }"
        >

          <!-- PAPER -->
          <div class="paper-content">
            <!-- Paper heading -->
            <div class="paper-header">
              <div class="paper-logo">
                SK
              </div>

              <div class="paper-title">
                {{ piece.title }}
              </div>
            </div>

            <!-- Lines -->
            <div class="paper-line"></div>
            <div class="paper-line"></div>
            <div class="paper-line short"></div>


            <!-- Content -->
            <div v-if="index === 0"class="paper-chart">
              <span></span>
              <span></span>
              <span></span>
              <span></span>
            </div>


            <div v-else-if="index === 1" class="paper-box">
            </div>


            <div v-else-if="index === 2"class="paper-map">
              <div class="map-dot"></div>
              <div class="map-line"></div>
              <div class="map-line two"></div>
            </div>

            <div v-else-if="index === 3"class="paper-circle">
            </div>

            <div v-else class="paper-box">
            </div>


            <!-- Bottom lines -->
            <div class="paper-line"></div>
            <div class="paper-line short"></div>
          </div>
        </div>
      </div>
    </div>


    <!--MAGNIFYING GlASS-->
    <div class="pointer-events-none fixed inset-0 z-10 flex items-center justify-center"
      :style="{
        opacity: glassOpacity
      }"
    >

      <img src="/MagnifyingGlass_white.png" class="h-[150px] w-[150px] object-contain"
        :style="{
          transform: `scale(${magglassScale})`
        }"
      />

    </div>


    <!--glass shattter-->
    <div class="pointer-events-none fixed inset-0 z-20"
      :style="{
        opacity: shardOpacity
      }"
    >

      <div  class="relative h-full w-full">
        <!-- TOP LEFT -->
        <div class="shard absolute left-[8%] top-[3%]  h-[240px] w-[320px]"
          :style="{
            clipPath:
              'polygon(0 0,85% 0,100% 45%,72% 100%,20% 75%)',
            transform: `
              translate(
                ${-distance * 0.8}px,
                ${-distance * 0.7}px
              )
              rotate(${shatter * -18}deg)
            `
          }"
        >
          <span class="shine"></span>
        </div>


        <!-- TOP CENTER -->
        <div class="shard absolute left-[40%] top-[-5%]  h-[280px] w-[250px]"
         :style="{
            clipPath:
              'polygon(10% 0,100% 0,80% 55%,50% 100%,5% 70%)',
            transform: `
              translate(
                ${distance * 0.1}px,
                ${-distance}px
              )
              rotate(${shatter * 25}deg)
            `
          }"
        >
          <span class="shine"></span>
        </div>


        <!-- TOP RIGHT -->
        <div class="shard absolute right-[8%] top-0  h-[280px] w-[310px]"
         :style="{
            clipPath:
              'polygon(0 0,100% 5%,90% 65%,45% 100%,20% 50%)',
            transform: `
              translate(
                ${distance * 0.9}px,
                ${-distance * 0.6}px
              )
              rotate(${shatter * 30}deg)
            `
          }"
        >
          <span class="shine"></span>
        </div>


        <!-- LEFT -->
        <div class="shard absolute left-[-2%] top-[28%] h-[280px] w-[300px]"
          :style="{
            clipPath:
              'polygon(0 20%,65% 0,100% 45%,85% 90%,20% 100%)',
            transform: `
              translate(
                ${-distance}px,
                ${-distance * 0.1}px
              )
              rotate(${shatter * -25}deg)
            `
          }"
        >
          <span class="shine"></span>
        </div>


        <!-- CENTER LEFT -->
        <div class="shard absolute left-[25%] top-[15%]  h-[300px] w-[280px]"
          :style="{
            clipPath:
              'polygon(0 5%,75% 0,100% 60%,65% 100%,5% 80%)',
            transform: `
              translate(
                ${-distance * 0.3}px,
                ${-distance * 0.1}px
              )
              rotate(${shatter * -12}deg)
            `
          }"
        >
          <span class="shine"></span>
        </div>


        <!-- CENTER -->
        <div class="shard absolute left-[42%] top-[30%]  h-[300px] w-[280px]"
          :style="{
            clipPath:
              'polygon(10% 0,90% 10%,100% 65%,65% 100%,20% 85%,0 40%)',
            transform: `
              translate(
                ${distance * 0.1}px,
                ${distance * 0.15}px
              )
              rotate(${shatter * 90}deg)
            `
          }"
        >
          <span class="shine"></span>
        </div>


        <!-- CENTER RIGHT -->
        <div class="shard absolute right-[25%] top-[20%] h-[300px] w-[280px]"
          :style="{
            clipPath:
              'polygon(10% 0,100% 15%,85% 75%,45% 100%,0 55%)',
            transform: `
              translate(
                ${distance * 0.7}px,
                ${-distance * 0.1}px
              )
              rotate(${shatter * 20}deg)
            `
          }"
        >
          <span class="shine"></span>
        </div>


        <!-- RIGHT -->
        <div class="shard absolute right-[-2%] top-[35%] h-[300px] w-[300px]"
          :style="{
            clipPath:
              'polygon(0 0,85% 10%,100% 60%,60% 100%,5% 75%)',
            transform: `
              translate(
                ${distance}px,
                ${distance * 0.1}px
              )
              rotate(${shatter * 35}deg)
            `
          }"
        >
          <span class="shine"></span>
        </div>


        <!-- BOTTOM LEFT -->
        <div class="shard absolute bottom-[-5%] left-[8%]  h-[280px] w-[320px]"       
          :style="{
            clipPath:
              'polygon(0 15%,55% 0,100% 35%,75% 100%,10% 80%)',
            transform: `
              translate(
                ${-distance * 0.8}px,
                ${distance * 0.8}px
              )
              rotate(${shatter * -30}deg)
            `
          }"
        >
          <span class="shine"></span>
        </div>


        <!-- BOTTOM CENTER -->
        <div class="shard absolute  bottom-[-8%] left-[38%]  h-[300px] w-[280px]"
         :style="{
            clipPath:
              'polygon(15% 0,90% 10%,100% 65%,55% 100%,0 75%)',
            transform: `
              translate(
                ${distance * 0.1}px,
                ${distance}px
              )
              rotate(${shatter * 25}deg)
            `
          }"
        >
          <span class="shine"></span>
        </div>


        <!-- BOTTOM RIGHT -->
        <div class="shard absolute  bottom-[-5%] right-[8%] h-[280px] w-[320px]"
          :style="{
            clipPath:
              'polygon(10% 0,100% 20%,85% 100%,25% 80%)',
            transform: `
              translate(
                ${distance * 0.8}px,
                ${distance * 0.8}px
              )
              rotate(${shatter * 35}deg)
            `
          }"
        >
          <span class="shine"></span>
        </div>


        <!-- SMALL LEFT -->
        <div class="shard absolute left-[18%] top-[55%]  h-[150px] w-[170px]"
          :style="{
            clipPath:
              'polygon(0 10%,70% 0,100% 60%,55% 100%,10% 75%)',
            transform: `
              translate(
                ${-distance * 1.1}px,
                ${distance * 0.4}px
              )
              rotate(${shatter * -40}deg)
            `
          }"
        >
          <span class="shine"></span>
        </div>


        <!-- SMALL RIGHT -->
        <div class="shard absolute  right-[18%] top-[55%]  h-[160px] w-[180px]"
         :style="{
            clipPath:
              'polygon(10% 0,100% 20%,80% 100%,0 70%)',
            transform: `
              translate(
                ${distance * 1.1}px,
                ${distance * 0.4}px
              )
              rotate(${shatter * 40}deg)
            `
          }"
        >
          <span class="shine"></span>
        </div>


        <!-- EXTRA LEFT -->

        <div class="shard absolute left-[30%] top-[65%] h-[120px] w-[150px]"
          :style="{
            clipPath:
              'polygon(5% 0,100% 25%,75% 100%,0 70%)',
            transform: `
              translate(
                ${-distance * 0.8}px,
                ${distance * 0.8}px
              )
              rotate(${shatter * -65}deg)
            `
          }"
        >
          <span class="shine"></span>
        </div>


        <!-- EXTRA RIGHT -->
        <div class="shard absolute right-[30%] top-[65%] h-[130px] w-[150px]"          
          :style="{
            clipPath:
              'polygon(15% 0,100% 10%,80% 100%,0 75%)',
            transform: `
              translate(
                ${distance * 0.8}px,
                ${distance * 0.8}px
              )
              rotate(${shatter * 65}deg)
            `
          }"
        >
          <span class="shine"></span>
        </div>
      </div>
    </div>


  <!--page-->

    <section class="relative z-30 flex min-h-[300vh] flex-col items-center">


      <!-- START -->

      <div  class="flex min-h-screen items-center justify-center">       
        <div class="text-center justify-center ">
          <img src="/SugboKlaroLogo_dark.png" class="h-[300px] w-[300px] object-contain mb-[100px] -translate-y-[100px]">
          <h1 class="text-5xl font-bold tracking-tight">
            Explore
          </h1>

          <p class="mt-4 text-slate-300">
            Scroll down
          </p>

        </div>

      </div>


      <!-- MIDDLE -->

      <div class="flex min-h-screen items-center justify-center">
       <div class="text-center">
          <h2 class="text-4xl font-bold text-sky-300">
            Discover
          </h2>

          <p class="mt-4 text-slate-300">
            Keep scrolling
          </p>

        </div>

      </div>


      <!-- END -->


        <div class="flex min-h-screen w-full items-center justify-center">
          <div class="relative z-30 w-full max-w-sm rounded-2xl border-2 border-[#37b5e7] bg-slate-800 p-8 text-center shadow-xl">
            <div class="flex flex-col items-center">
              <img src="/SugboKlaroLogo_dark.png" class="w-48 object-contain"/>

              <p class="mt-4 text-slate-300">
                The quick brown fox jumps over the lazy dog
              </p>

              <p class="mb-6 mt-2 text-sm text-slate-400">
                The quick brown fox jumps over the lazy dog
                the quick brown fox jumps over the lazy dog
              </p>

              <!-- BUTTON -->
              
              <button 
                @click="$router.push('/dashboard')" 
                class="rounded-lg bg-[#37b5e7] px-6 py-3 font-semibold text-slate-900 transition-all duration-300 hover:scale-105 hover:bg-sky-300 active:scale-95">
                Explore Now
              </button>
         
              
            </div>
          </div>
        </div>
    </section>
  </main>
</template>


<style>

/* =========================================================
   GLASS SHARDS
========================================================= */

.shard {
  overflow: hidden;

  background:
    linear-gradient(
      135deg,
      rgba(220, 235, 250, 0.42),
      rgba(100, 150, 195, 0.25) 40%,
      rgba(40, 80, 125, 0.18) 75%,
      rgba(220, 235, 250, 0.32)
    );

  border:
    1px solid
    rgba(230, 240, 250, 0.45);

  box-shadow:
    inset 0 0 35px
    rgba(220, 235, 250, 0.12),

    0 0 25px
    rgba(120, 175, 220, 0.12);

  backdrop-filter: blur(4px);

  animation:
    shard-float
    4s ease-in-out
    infinite alternate;
}


/* GLASS FLOAT*/

@keyframes shard-float {

  0% {
    translate: 0 0;
  }

  25% {
    translate: 18px -12px;
  }

  50% {
    translate: -12px 18px;
  }

  75% {
    translate: 22px 10px;
  }

  100% {
    translate: -15px -18px;
  }

}


/* SHARD SPEEDS*/

.shard:nth-child(1) {
  animation-duration: 4.5s;
}

.shard:nth-child(2) {
  animation-duration: 5.2s;
  animation-delay: -1s;
}

.shard:nth-child(3) {
  animation-duration: 3.8s;
  animation-delay: -2s;
}

.shard:nth-child(4) {
  animation-duration: 5.8s;
  animation-delay: -3s;
}

.shard:nth-child(5) {
  animation-duration: 4.2s;
  animation-delay: -1.5s;
}

.shard:nth-child(6) {
  animation-duration: 6s;
  animation-delay: -2.5s;
}

.shard:nth-child(7) {
  animation-duration: 4.8s;
  animation-delay: -0.5s;
}

.shard:nth-child(8) {
  animation-duration: 5.5s;
  animation-delay: -3.5s;
}

.shard:nth-child(9) {
  animation-duration: 4s;
  animation-delay: -1.8s;
}

.shard:nth-child(10) {
  animation-duration: 6.2s;
  animation-delay: -4s;
}

.shard:nth-child(11) {
  animation-duration: 4.6s;
  animation-delay: -2.2s;
}

.shard:nth-child(12) {
  animation-duration: 5.7s;
  animation-delay: -0.8s;
}


/* GLASS REFLECTION*/

.shine {
  position: absolute;

  left: 20%;
  top: -20%;

  width: 8%;
  height: 140%;

  background:
    rgba(255, 255, 255, 0.4);

  transform: rotate(25deg);

  filter: blur(4px);
}


/*CUBE*/

.cube-face {
  border:
    1px solid
    rgba(186, 230, 253, 0.9);

  box-shadow:
    inset 0 0 25px
    rgba(255, 255, 255, 0.25),

    0 0 30px
    rgba(56, 189, 248, 0.35);

  backface-visibility: visible;
}


/*CUBE ROTATION*/

@keyframes cube-rotate {

  from {
    transform:
      rotateX(-20deg)
      rotateY(0deg);
  }

  to {
    transform:
      rotateX(-20deg)
      rotateY(360deg);
  }

}


/* DOCUMENT PIECES */

.document-piece {

  transform-origin: center center;

  will-change:
    transform,
    opacity;
}


/* PAPER */

.paper-content {

  position: relative;

  width: 100%;
  height: 100%;

  padding: 14px;

  overflow: hidden;

  border:
    1px solid
    rgba(255, 255, 255, 0.8);

  border-radius: 4px;

  background:
    linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.97),
      rgba(226, 239, 248, 0.94)
    );

  color: #164e63;

  box-shadow:
    0 15px 40px
    rgba(0, 0, 0, 0.35),

    inset 0 0 20px
    rgba(14, 116, 144, 0.08);

  transform-origin: center;

}


/* PAPER HEADER */

.paper-header {

  display: flex;

  align-items: center;

  gap: 8px;

  margin-bottom: 12px;
}


.paper-logo {

  display: flex;

  align-items: center;

  justify-content: center;

  width: 25px;
  height: 25px;

  border-radius: 5px;

  background:
    #38bdf8;

  color: white;

  font-size: 9px;

  font-weight: 800;
}


.paper-title {

  font-size: 12px;

  font-weight: 800;

  letter-spacing: 0.5px;
}


/* PAPER LINES */

.paper-line {

  width: 100%;

  height: 5px;

  margin-top: 8px;

  border-radius: 999px;

  background:
    rgba(14, 116, 144, 0.18);
}


.paper-line.short {
  width: 60%;
}


.paper-line.medium {
  width: 78%;
}


/* PAPER BOX*/

.paper-box {

  width: 100%;

  height: 55px;

  margin-top: 12px;

  border-radius: 4px;

  border:
    1px solid
    rgba(14, 116, 144, 0.2);

  background:
    rgba(56, 189, 248, 0.12);
}


/* PAPER CHART */

.paper-chart {

  display: flex;

  align-items: flex-end;

  gap: 6px;

  height: 55px;

  margin-top: 12px;

  padding:
    8px;

  border:
    1px solid
    rgba(14, 116, 144, 0.15);

  background:
    rgba(56, 189, 248, 0.08);
}


.paper-chart span {

  width: 14px;

  border-radius:
    3px 3px 0 0;

  background:
    #38bdf8;
}


.paper-chart span:nth-child(1) {
  height: 30%;
}

.paper-chart span:nth-child(2) {
  height: 60%;
}

.paper-chart span:nth-child(3) {
  height: 45%;
}

.paper-chart span:nth-child(4) {
  height: 80%;
}


/* PAPER MAP*/

.paper-map {

  position: relative;

  height: 60px;

  margin-top: 12px;

  overflow: hidden;

  border:
    1px solid
    rgba(14, 116, 144, 0.2);

  border-radius: 4px;

  background:
    linear-gradient(
      135deg,
      rgba(56, 189, 248, 0.15),
      rgba(14, 116, 144, 0.08)
    );
}


.map-dot {

  position: absolute;

  left: 50%;

  top: 50%;

  width: 10px;

  height: 10px;

  border-radius: 50%;

  background:
    #ef4444;

  transform:
    translate(-50%, -50%);

  box-shadow:
    0 0 10px
    rgba(239, 68, 68, 0.5);
}


.map-line {

  position: absolute;

  left: 10%;

  top: 30%;

  width: 80%;

  height: 2px;

  background:
    rgba(14, 116, 144, 0.25);

  transform:
    rotate(25deg);
}


.map-line.two {

  top: 65%;

  transform:
    rotate(-20deg);
}


/* paper cricle*/

.paper-circle {

  width: 55px;

  height: 55px;

  margin:
    12px auto;

  border-radius: 50%;

  border:
    5px solid
    rgba(56, 189, 248, 0.45);

  border-right-color:
    #38bdf8;

  border-bottom-color:
    #38bdf8;
}

@media (max-width: 768px) {

  .shard {
    opacity: 0.75;
  }

  .document-piece {
    transform-origin: center;
  }

}

</style>