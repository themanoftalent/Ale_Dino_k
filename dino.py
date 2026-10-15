import os

# Define the project structure and file contents
project_name = "DinoJump"

files = {
    ".idx/dev.nix": r"""# This file configures the Project IDX environment
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-23.11";

  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.zulu17
    pkgs.android-tools
    pkgs.gradle
  ];

  # Sets environment variables in the workspace
  env = {
    # Project IDX handles the SDK path internally, but we can define java home if needed
    JAVA_HOME = "${pkgs.zulu17}/lib/openjdk";
  };

  idx = {
    # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
    extensions = [
      "vscjava.vscode-java-pack"
      "mathiasfrohlich.Kotlin"
      "fwcd.kotlin"
      "vscjava.vscode-gradle"
    ];

    workspace = {
      # Runs when you create/open the workspace
      onCreate = {
        build-app = "./gradlew assembleDebug";
      };
    };

    # Enable previews
    previews = {
      enable = true;
      previews = {
        android = {
          command = ["./gradlew" "assembleDebug"];
          manager = "android";
        };
      };
    };
  };
}
""",
    "build.gradle": r"""// Top-level build file where you can add configuration options common to all sub-projects/modules.
plugins {
    id 'com.android.application' version '8.2.0' apply false
    id 'org.jetbrains.kotlin.android' version '1.9.20' apply false
    id 'com.google.gms.google-services' version '4.4.0' apply false
}
""",
    "app/build.gradle": r"""plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
    id 'com.google.gms.google-services'
}

android {
    namespace 'com.example.dinojump'
    compileSdk 34

    defaultConfig {
        applicationId "com.example.dinojump"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
    kotlinOptions {
        jvmTarget = '1.8'
    }
    buildFeatures {
        compose true
    }
    composeOptions {
        kotlinCompilerExtensionVersion '1.5.5'
    }
}

dependencies {
    // Core Android & Compose
    implementation platform('androidx.compose:compose-bom:2024.02.00')
    implementation 'androidx.activity:activity-compose:1.8.2'
    implementation 'androidx.compose.ui:ui'
    implementation 'androidx.compose.ui:ui-graphics'
    implementation 'androidx.compose.ui:ui-tooling-preview'
    implementation 'androidx.compose.material3:material3'
    implementation 'androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0'

    // Firebase
    implementation platform('com.google.firebase:firebase-bom:32.7.2')
    implementation 'com.google.firebase:firebase-analytics'
    implementation 'com.google.firebase:firebase-auth'
    implementation 'com.google.firebase:firebase-firestore'
    
    // Icons (Optional but useful)
    implementation 'androidx.compose.material:material-icons-extended'
}
""",
    "app/src/main/AndroidManifest.xml": r"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <!-- Internet required for Firebase -->
    <uses-permission android:name="android.permission.INTERNET" />

    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="Dino Jump"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@android:style/Theme.NoTitleBar.Fullscreen"
        tools:targetApi="31">
        
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:screenOrientation="portrait"
            android:theme="@android:style/Theme.NoTitleBar.Fullscreen">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
""",
    "app/src/main/res/drawable/ic_dino.xml": r"""<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="100dp"
    android:height="100dp"
    android:viewportWidth="24"
    android:viewportHeight="24">
    <path
        android:fillColor="#4CAF50"
        android:pathData="M20.6,18.7c-0.3,-1 -0.6,-2.2 -2.6,-2.2c-1.5,0 -1.8,0.3 -1.8,0.3l-0.8,-4.9c1.8,-0.8 2.7,-2.7 2,-4.6c-0.7,-1.9 -2.9,-3 -4.8,-2.2c-0.7,0.3 -1.3,0.8 -1.6,1.4C10.6,6.1 10.3,6 10,6C8.9,6 8,6.9 8,8v6.5c-0.3,0.1 -0.6,0.3 -0.8,0.5L5,16.8c-0.9,0.9 -0.9,2.3 0,3.2l0,0l14.1,0C20.5,19.8 20.8,19.2 20.6,18.7z"/>
    <path
        android:fillColor="#388E3C"
        android:pathData="M15,7.5m-1,0a1,1 0 1,1 2,0a1,1 0 1,1 -2,0"/>
</vector>
""",
    "app/src/main/res/drawable/ic_star_item.xml": r"""<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="64dp"
    android:height="64dp"
    android:viewportWidth="24"
    android:viewportHeight="24">
    <path
        android:fillColor="#FFD700"
        android:pathData="M12,17.27L18.18,21l-1.64,-7.03L22,9.24l-7.19,-0.61L12,2L9.19,8.63L2,9.24l5.46,4.73L5.82,21z"/>
    <path
        android:strokeColor="#FFA000"
        android:strokeWidth="1"
        android:pathData="M12,17.27L18.18,21l-1.64,-7.03L22,9.24l-7.19,-0.61L12,2L9.19,8.63L2,9.24l5.46,4.73L5.82,21z"/>
</vector>
""",
    "app/src/main/java/com/example/dinojump/FirebaseRepository.kt": r"""package com.example.dinojump

import android.util.Log
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.SetOptions
import kotlinx.coroutines.tasks.await
import java.util.Date

/**
 * Handles anonymous authentication and saving scores.
 * Designed to fail silently so the toddler can still play if offline.
 */
class FirebaseRepository {

    private val auth: FirebaseAuth by lazy { FirebaseAuth.getInstance() }
    private val db: FirebaseFirestore by lazy { FirebaseFirestore.getInstance() }

    // Ensure user is signed in
    suspend fun ensureAnonymousLogin(): String? {
        return try {
            if (auth.currentUser == null) {
                val result = auth.signInAnonymously().await()
                Log.d("Firebase", "Signed in anonymously: ${result.user?.uid}")
                result.user?.uid
            } else {
                auth.currentUser?.uid
            }
        } catch (e: Exception) {
            Log.e("Firebase", "Login failed", e)
            null
        }
    }

    suspend fun saveHighScore(score: Int) {
        val uid = ensureAnonymousLogin() ?: return // If login fails, stop

        val userScoreRef = db.collection("users").document(uid)

        try {
            // Check current high score first
            val snapshot = userScoreRef.get().await()
            val currentHigh = snapshot.getLong("highScore") ?: 0L

            if (score > currentHigh) {
                val data = hashMapOf(
                    "highScore" to score,
                    "lastPlayed" to Date()
                )
                userScoreRef.set(data, SetOptions.merge()).await()
                Log.d("Firebase", "New high score saved: $score")
            }
        } catch (e: Exception) {
            Log.e("Firebase", "Failed to save score", e)
        }
    }

    suspend fun getHighScore(): Int {
        val uid = ensureAnonymousLogin() ?: return 0
        return try {
            val snapshot = db.collection("users").document(uid).get().await()
            snapshot.getLong("highScore")?.toInt() ?: 0
        } catch (e: Exception) {
            0
        }
    }
}
""",
    "app/src/main/java/com/example/dinojump/GameViewModel.kt": r"""package com.example.dinojump

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlin.random.Random

// Simple data class for a collectible item
data class Collectible(
    val id: Long = System.currentTimeMillis(),
    val xPercent: Float, // 0.0 to 1.0 (Horizontal position)
    val yPercent: Float  // 0.0 to 1.0 (Vertical position)
)

class GameViewModel : ViewModel() {

    private val repository = FirebaseRepository()

    // Game State
    var score by mutableStateOf(0)
        private set

    var highScore by mutableStateOf(0)
        private set

    // Anti-Gravity Mode (New)
    var isAntiGravity by mutableStateOf(false)
        private set

    // Dino State
    var isDinoJumping by mutableStateOf(false)
        private set

    // List of stars on screen
    var collectibles by mutableStateOf(listOf<Collectible>())
        private set

    private var gameLoopJob: Job? = null

    init {
        // Load high score on init
        viewModelScope.launch {
            highScore = repository.getHighScore()
        }
        startGameLoop()
    }

    /**
     * The main "brain" of the game.
     * Spawns items periodically.
     */
    private fun startGameLoop() {
        gameLoopJob?.cancel()
        gameLoopJob = viewModelScope.launch {
            while (true) {
                delay(2000) // Every 2 seconds, maybe spawn a star
                if (collectibles.size < 3) { // Max 3 stars on screen to keep it simple
                    spawnCollectible()
                }
            }
        }
    }

    private fun spawnCollectible() {
        val newItem = Collectible(
            // Random position but keep away from edges (0.1 to 0.9)
            xPercent = Random.nextFloat() * 0.8f + 0.1f,
            yPercent = Random.nextFloat() * 0.5f + 0.1f // Keep in upper 60% of screen
        )
        collectibles = collectibles + newItem
    }

    /**
     * Called when the user taps the screen (not on a star).
     * Makes the dino jump.
     */
    fun onScreenTap() {
        if (isDinoJumping) return // Already in air

        viewModelScope.launch {
            isDinoJumping = true
            // Float longer if antigravity is on (1.5s vs 0.6s)
            val duration = if (isAntiGravity) 1500L else 600L
            delay(duration) 
            isDinoJumping = false
        }
    }

    // New Toggle Function
    fun toggleAntiGravity() {
        isAntiGravity = !isAntiGravity
    }

    /**
     * Called when the user taps a specific star.
     */
    fun onCollectibleTapped(item: Collectible) {
        // Remove the item
        collectibles = collectibles.filter { it.id != item.id }
        
        // Increase score
        score++

        // Check high score logic
        if (score > highScore) {
            highScore = score
            saveHighScore()
        }
    }

    private fun saveHighScore() {
        viewModelScope.launch {
            repository.saveHighScore(highScore)
        }
    }

    override fun onCleared() {
        super.onCleared()
        gameLoopJob?.cancel()
    }
}
""",
    "app/src/main/java/com/example/dinojump/MainActivity.kt": r"""package com.example.dinojump

import android.media.AudioAttributes
import android.media.SoundPool
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Image
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.RocketLaunch
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*

class MainActivity : ComponentActivity() {
    
    private val viewModel: GameViewModel by viewModels()
    private lateinit var soundPool: SoundPool
    private var soundJump: Int = 0
    private var soundCollect: Int = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Setup Audio
        val audioAttributes = AudioAttributes.Builder()
            .setUsage(AudioAttributes.USAGE_GAME)
            .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
            .build()

        soundPool = SoundPool.Builder()
            .setMaxStreams(5)
            .setAudioAttributes(audioAttributes)
            .build()

        // NOTE: For a real app, put .mp3 files in res/raw.
        // Since I cannot generate MP3s, I am creating a safe fallback.
        // If you add "jump.mp3" and "ping.mp3" to res/raw, un-comment the lines below.
        
        // soundJump = soundPool.load(this, R.raw.jump, 1) 
        // soundCollect = soundPool.load(this, R.raw.ping, 1)

        setContent {
            MaterialTheme {
                DinoGameScreen(
                    viewModel = viewModel,
                    onPlayJumpSound = { playSound(soundJump) },
                    onPlayCollectSound = { playSound(soundCollect) }
                )
            }
        }
    }

    private fun playSound(soundId: Int) {
        if (soundId != 0) {
            soundPool.play(soundId, 1f, 1f, 0, 0, 1f)
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        soundPool.release()
    }
}

@Composable
fun DinoGameScreen(
    viewModel: GameViewModel,
    onPlayJumpSound: () -> Unit,
    onPlayCollectSound: () -> Unit
) {
    val configuration = LocalConfiguration.current
    val screenHeight = configuration.screenHeightDp.dp

    // Observe State
    val isJumping = viewModel.isDinoJumping
    val isAntiGravity = viewModel.isAntiGravity // New state
    val collectibles = viewModel.collectibles
    val score = viewModel.score
    val highScore = viewModel.highScore

    // Animation Settings based on Gravity Mode
    // Normal: 300ms up, -200dp height
    // Anti-Gravity: 1500ms up, -400dp height (Moon physics!)
    val jumpTarget = if (isAntiGravity) (-400).dp else (-200).dp
    val animDuration = if (isAntiGravity) 1500 else 300

    // Animation for Jump
    // If jumping, move up (negative offset), else stay at bottom (0)
    val dinoOffsetY by animateDpAsState(
        targetValue = if (isJumping) jumpTarget else 0.dp,
        animationSpec = tween(durationMillis = animDuration),
        label = "Jump Animation",
        finishedListener = { }
    )

    // Trigger sound when jump starts
    LaunchedEffect(isJumping) {
        if (isJumping) onPlayJumpSound()
    }

    // Main Game Container
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                brush = Brush.verticalGradient(
                    colors = if (isAntiGravity) {
                        // Space Theme
                        listOf(Color(0xFF1A237E), Color(0xFF4527A0)) 
                    } else {
                        // Sky Theme
                        listOf(Color(0xFF87CEEB), Color(0xFFE0F7FA))
                    }
                )
            )
            .clickable(
                interactionSource = remember { MutableInteractionSource() },
                indication = null // Remove ripple effect
            ) {
                viewModel.onScreenTap()
            }
    ) {
        
        // 1. The Ground
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(100.dp)
                .align(Alignment.BottomCenter)
                .background(Color(0xFF5D4037)) // Dirt brown
        ) {
            // Grass strip
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(20.dp)
                    .align(Alignment.TopCenter)
                    .background(Color(0xFF7CB342))
            )
        }

        // 2. The Dino
        Image(
            painter = painterResource(id = R.drawable.ic_dino),
            contentDescription = "Dino",
            modifier = Modifier
                .size(120.dp) // Big for toddlers
                .align(Alignment.BottomCenter)
                .offset(y = dinoOffsetY - 50.dp) // -50dp to sit on grass, plus jump offset
        )

        // 3. Collectibles (Stars)
        collectibles.forEach { item ->
            CollectibleItem(
                item = item,
                onTap = {
                    viewModel.onCollectibleTapped(item)
                    onPlayCollectSound()
                }
            )
        }

        // 4. Score Board (Top Left)
        Column(
            modifier = Modifier
                .padding(24.dp)
                .align(Alignment.TopStart)
        ) {
            Text(
                text = "Stars: $score",
                fontSize = 32.sp,
                fontWeight = FontWeight.Bold,
                color = if (isAntiGravity) Color.White else Color(0xFFFF6F00)
            )
            if (highScore > 0) {
                Text(
                    text = "Best: $highScore",
                    fontSize = 20.sp,
                    fontWeight = FontWeight.Medium,
                    color = if (isAntiGravity) Color.Yellow else Color(0xFFBF360C)
                )
            }
        }

        // 5. Anti-Gravity Toggle (Top Right)
        IconButton(
            onClick = { viewModel.toggleAntiGravity() },
            modifier = Modifier
                .align(Alignment.TopEnd)
                .padding(24.dp)
                .size(64.dp) // Big button for toddler
        ) {
            Icon(
                imageVector = Icons.Filled.RocketLaunch,
                contentDescription = "Anti-Gravity Mode",
                tint = if (isAntiGravity) Color.Yellow else Color.White,
                modifier = Modifier.fillMaxSize()
            )
        }
    }
}

@Composable
fun CollectibleItem(item: Collectible, onTap: () -> Unit) {
    // Convert relative percentage to Alignment bias (-1 to 1)
    // input 0..1 -> output -1..1
    val biasX = (item.xPercent * 2) - 1
    val biasY = (item.yPercent * 2) - 1

    Box(
        modifier = Modifier
            .fillMaxSize()
            .padding(top = 50.dp, bottom = 150.dp) // Keep away from very top and floor
    ) {
        Image(
            painter = painterResource(id = R.drawable.ic_star_item),
            contentDescription = "Star",
            modifier = Modifier
                .align(Alignment(biasX, biasY))
                .size(80.dp) // Big touch target
                .clickable(
                    interactionSource = remember { MutableInteractionSource() },
                    indication = null
                ) { onTap() }
        )
    }
}
""",
    ".gitignore": r"""*.iml
.gradle
/local.properties
/.idea/caches
/.idea/libraries
/.idea/modules.xml
/.idea/workspace.xml
/.idea/navEditor.xml
/.idea/assetWizardSettings.xml
.DS_Store
/build
/captures
.externalNativeBuild
.cxx
local.properties
"""
}

def create_project():
    base_dir = project_name
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    for filepath, content in files.items():
        full_path = os.path.join(base_dir, filepath)
        directory = os.path.dirname(full_path)
        
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created: {full_path}")

    print(f"\nProject '{project_name}' created successfully!")
    print("Don't forget to add your 'google-services.json' to the 'app' folder.")

if __name__ == "__main__":
    create_project()