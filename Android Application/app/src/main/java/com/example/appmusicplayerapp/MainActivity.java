package com.example.appmusicplayerapp;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.content.Intent;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button StartButton = findViewById(R.id.start_button);
        StartButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startmusicplayer();
            }
    });
    }
    private void startmusicplayer() {
        Intent intent = new Intent(this, musicplayer.class);
        startActivity(intent);
    }
}