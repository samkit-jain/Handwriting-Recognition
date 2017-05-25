package jain.samkit.handwritingrecognition;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.drawable.BitmapDrawable;
import android.media.ThumbnailUtils;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.MotionEvent;
import android.view.View;
import android.widget.ImageView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.Socket;

public class MainActivity extends AppCompatActivity {

    private final String IP_ADDR = "192.168.43.214";
    private final int IP_ADDR_PORT = 8080;
    DrawingView dv;
    private Paint mPaint;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        dv = new DrawingView(this);
        setContentView(dv);
        mPaint = new Paint();
        mPaint.setAntiAlias(true);
        mPaint.setDither(true);
        mPaint.setColor(Color.WHITE);
        mPaint.setStyle(Paint.Style.STROKE);
        mPaint.setStrokeJoin(Paint.Join.ROUND);
        mPaint.setStrokeCap(Paint.Cap.ROUND);
        mPaint.setStrokeWidth(80);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case R.id.predict:
                //Toast.makeText(getApplicationContext(), "YO SUP", Toast.LENGTH_SHORT).show();
                dv.saveDrawing();
                return true;
            default:
                return super.onOptionsItemSelected(item);
        }
    }

    /*
    private void callPuter(final String str) {
        Thread t = new Thread(){
            @Override
            public void run() {
                try {
                    InetAddress serverAddr = InetAddress.getByName(IP_ADDR);
                    Socket s = new Socket();
                    s.connect(new InetSocketAddress(serverAddr, IP_ADDR_PORT), 5000);
                    DataOutputStream dos = new DataOutputStream(s.getOutputStream());
                    byte[] buf = str.getBytes("UTF-8");
                    dos.write(buf, 0, buf.length);

                    //read input stream
                    //DataInputStream dis2 = new DataInputStream(s.getInputStream());
                    //InputStreamReader disR2 = new InputStreamReader(dis2);
                    //BufferedReader br = new BufferedReader(disR2);//create a BufferReader object for input

                    //print the input to the application screen
                    //final TextView receivedMsg = (TextView) findViewById(R.id.textView2);
                    //receivedMsg.setText(br.toString());
                    //Log.v("tagga", br.toString());

                    //dis2.close();
                    s.close();

                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        };

        t.start();
    }
    */

    public class DrawingView extends View {

        public int width;
        public int height;
        private Bitmap mBitmap;
        private Canvas mCanvas;
        private Path mPath;
        private Paint mBitmapPaint;
        Context context;
        private Paint circlePaint;
        private Path circlePath;

        public DrawingView(Context c) {
            super(c);
            context = c;
            mPath = new Path();
            mBitmapPaint = new Paint(Paint.DITHER_FLAG);
            circlePaint = new Paint();
            circlePath = new Path();
            circlePaint.setAntiAlias(true);
            circlePaint.setColor(Color.BLUE);
            circlePaint.setStyle(Paint.Style.STROKE);
            circlePaint.setStrokeJoin(Paint.Join.MITER);
            circlePaint.setStrokeWidth(4f);
        }

        public void saveDrawing() {
            Bitmap b = mBitmap;
            b = ThumbnailUtils.extractThumbnail(b, 256, 256);
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            b.compress(Bitmap.CompressFormat.PNG, 100, baos);
            byte[] yourByteArray;
            yourByteArray = baos.toByteArray();

            callPuter(yourByteArray);
        }

        private void callPuter(final byte[] str) {
            Thread t = new Thread() {
                @Override
                public void run() {
                    try {
                        InetAddress serverAddr = InetAddress.getByName(IP_ADDR);
                        Socket s = new Socket();
                        s.connect(new InetSocketAddress(serverAddr, IP_ADDR_PORT), 5000);
                        DataOutputStream dos = new DataOutputStream(s.getOutputStream());
                        dos.writeInt(str.length);
                        dos.write(str, 0, str.length);

                        /*
                        //read input stream
                        DataInputStream dis2 = new DataInputStream(s.getInputStream());
                        InputStreamReader disR2 = new InputStreamReader(dis2);
                        BufferedReader br = new BufferedReader(disR2);//create a BufferReader object for input

                        //cannot call here
                        Toast.makeText(getApplicationContext(), br.toString(), Toast.LENGTH_SHORT).show();

                        dis2.close();
                        */
                        s.close();

                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            };

            t.start();
        }

        @Override
        protected void onSizeChanged(int w, int h, int oldw, int oldh) {
            super.onSizeChanged(w, h, oldw, oldh);

            mBitmap = Bitmap.createBitmap(w, h, Bitmap.Config.RGB_565);
            mCanvas = new Canvas(mBitmap);
        }

        @Override
        protected void onDraw(Canvas canvas) {
            super.onDraw(canvas);

            canvas.drawRGB(0, 0, 0);
            canvas.drawBitmap(mBitmap, 0, 0, mBitmapPaint);
            canvas.drawPath(mPath, mPaint);
            canvas.drawPath(circlePath, circlePaint);
        }

        private float mX, mY;
        private static final float TOUCH_TOLERANCE = 4;

        private void touch_start(float x, float y) {
            mPath.reset();
            mPath.moveTo(x, y);
            mX = x;
            mY = y;
        }

        private void touch_move(float x, float y) {
            float dx = Math.abs(x - mX);
            float dy = Math.abs(y - mY);
            if (dx >= TOUCH_TOLERANCE || dy >= TOUCH_TOLERANCE) {
                mPath.quadTo(mX, mY, (x + mX) / 2, (y + mY) / 2);
                mX = x;
                mY = y;

                circlePath.reset();
                circlePath.addCircle(mX, mY, 30, Path.Direction.CW);
            }
        }

        private void touch_up() {
            mPath.lineTo(mX, mY);
            circlePath.reset();
            // commit the path to our offscreen
            mCanvas.drawPath(mPath, mPaint);
            // kill this so we don't double draw
            mPath.reset();
        }

        @Override
        public boolean onTouchEvent(MotionEvent event) {
            float x = event.getX();
            float y = event.getY();

            switch (event.getAction()) {
                case MotionEvent.ACTION_DOWN:
                    touch_start(x, y);
                    invalidate();
                    break;
                case MotionEvent.ACTION_MOVE:
                    touch_move(x, y);
                    invalidate();
                    break;
                case MotionEvent.ACTION_UP:
                    touch_up();
                    invalidate();
                    break;
            }
            return true;
        }
    }
}
