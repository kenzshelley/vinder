package vinder.vinder;

import android.app.Activity;
import android.content.Intent;
import android.media.MediaPlayer;
import android.media.MediaRecorder;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import org.apache.http.Header;

import com.firebase.client.DataSnapshot;
import com.firebase.client.Firebase;
import com.firebase.client.FirebaseError;
import com.firebase.client.ValueEventListener;
import com.loopj.android.http.*;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class VoiceRecordActivity extends Activity {
    private Button mRecordButton;
    private Button mPlayButton;
    private Button mSendButton;
    private EditText mEmailField;

    private MediaRecorder mRecorder;
    private MediaPlayer mMediaPlayer;

    private String mFileName;

    boolean mIsRecording;

    Firebase mFirebaseRef;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_voice_record);

        mFirebaseRef = new Firebase("https://vinder.firebaseio.com");


        mFileName = Environment.getExternalStorageDirectory().getAbsolutePath();
        mFileName += "/voicefile.wav";

        mRecordButton = (Button)findViewById(R.id.record_voice_button);
        mPlayButton = (Button)findViewById(R.id.play_voice_button);
        mSendButton = (Button)findViewById(R.id.send_voice_button);
        mEmailField = (EditText) findViewById(R.id.edit_email_field);

        mRecordButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (mIsRecording){
                    mRecordButton.setText(R.string.start_record_voice);
                    mIsRecording = false;
                    stopRecording();
                } else {
                    mRecordButton.setText(R.string.stop_record_voice);
                    mIsRecording = true;
                    startRecording();
                }

            }
        });

        mPlayButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                startPlaying();
            }
        });

        mSendButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                File soundFile = new File(mFileName);
                RequestParams params = new RequestParams();

                String emailAddress = mEmailField.getText().toString();

                String hashedEmailAddress = "FAILED HASHING";
                try {
                    // Create MD5 Hash
                    MessageDigest digest = java.security.MessageDigest
                            .getInstance("MD5");
                    digest.update(emailAddress.getBytes());
                    byte messageDigest[] = digest.digest();

                    // Create Hex String
                    StringBuilder hexString = new StringBuilder();
                    for (byte aMessageDigest : messageDigest) {
                        String h = Integer.toHexString(0xFF & aMessageDigest);
                        while (h.length() < 2)
                            h = "0" + h;
                        hexString.append(h);
                    }
                    hashedEmailAddress = hexString.toString();

                } catch (NoSuchAlgorithmException e) {
                    e.printStackTrace();
                }
                mFirebaseRef.child("users").child(hashedEmailAddress).addValueEventListener(new ValueEventListener() {
                    @Override
                    public void onDataChange(DataSnapshot dataSnapshot) {

                        //extract all of the data from the dataSnapshot
                        ArrayList<String> emailMatches = new ArrayList<String>();
                        Iterator<DataSnapshot> emailMatchIterator = dataSnapshot.child("matches").getChildren().iterator();

                        while (emailMatchIterator.hasNext()) {
                            emailMatches.add(emailMatchIterator.next().getName());
                        }
                        if (!emailMatches.isEmpty()) {
                            Intent intent = new Intent(getApplicationContext(), MatchActivity.class);
                            intent.putExtra("email_address", dataSnapshot.getName());
                            intent.putExtra("mp3_url", dataSnapshot.child("mp3_url").getName());

                            intent.putStringArrayListExtra("match_emails", emailMatches);
                            startActivity(intent);
                        }
                    }

                    @Override
                    public void onCancelled(FirebaseError firebaseError) {

                    }
                });

                try {
                    params.put("sound_data", soundFile);
                    params.put("email_address", emailAddress);
                } catch (FileNotFoundException e){
                    Log.e("async", e.getLocalizedMessage());
                }

                AsyncHttpClient client = new AsyncHttpClient();

                String url = new String ("http://agile-peak-2922.herokuapp.com/receive_mp3");
                client.post(url, params, new AsyncHttpResponseHandler() {
                    @Override
                    public void onSuccess(int i, Header[] headers, byte[] bytes) {
                        String responseText = new String(bytes);
                        Toast t = Toast.makeText(getApplicationContext(),"SUCCESS: " + responseText, Toast.LENGTH_SHORT);
                        t.show();
                    }

                    @Override
                    public void onFailure(int i, Header[] headers, byte[] bytes, Throwable throwable) {
                        String responseText = new String(bytes);
                        Toast t = Toast.makeText(getApplicationContext(),"FAILURE: " + responseText, Toast.LENGTH_SHORT);
                        t.show();
                    }
                });
            }
        });
    }

    private void startRecording() {
        mRecorder = new MediaRecorder();
        mRecorder.setAudioSource(MediaRecorder.AudioSource.MIC);
        mRecorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
        mRecorder.setOutputFile(mFileName);
        mRecorder.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB);

        try {
            mRecorder.prepare();
        } catch (IOException e) {
            Log.e("MediaRecorder", "prepare() failed");
        }

        mRecorder.start();
    }

    private void stopRecording(){
        mRecorder.stop();
        mRecorder.release();
        mRecorder = null;
    }


    private void startPlaying() {
        mMediaPlayer = new MediaPlayer();
        mMediaPlayer.setOnCompletionListener(new MediaPlayer.OnCompletionListener() {
            @Override
            public void onCompletion(MediaPlayer mediaPlayer) {
                mMediaPlayer.release();
                mMediaPlayer = null;
                Log.d("MediaPlayer", "released");
            }
        });

        try {
            mMediaPlayer.setDataSource(mFileName);
            mMediaPlayer.prepare();
            mMediaPlayer.start();
        } catch (IOException e) {
            Log.e("MediaPlayer", "prepare() failed");
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.voice_record, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.action_settings) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
