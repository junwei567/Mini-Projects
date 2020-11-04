package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.Random;
import java.util.Date;

public class MainActivity extends AppCompatActivity {

//    TextView textView = findViewById(R.id.textViewRandomImages);
    Button button;
    ArrayList<Integer> images;
    ImageView myImage;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        button = findViewById(R.id.myButt);
        myImage = findViewById(R.id.myImage);
        images = new ArrayList<Integer>();
        images.add(R.drawable.bulbasaur);
        images.add(R.drawable.gyrados);
        images.add(R.drawable.snorlax);

        button.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    Date d = new Date();
                    Random r = new Random(d.getTime());
                    int i = r.nextInt(images.size());
                    myImage.setImageResource(images.get(i));
                }
        });
    }

}