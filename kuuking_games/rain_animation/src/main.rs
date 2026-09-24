use macroquad::prelude::*;

struct Heart {
    x: f32,
    y: f32,
    size: f32,
    speed: f32,
    drift: f32,
    phase: f32,
    color: Color,
}

impl Heart {
    fn new(width: f32, height: f32) -> Self {
        let mut heart = Self {
            x: 0.0,
            y: 0.0,
            size: 0.0,
            speed: 0.0,
            drift: 0.0,
            phase: 0.0,
            color: RED,
        };
        heart.reset(width, height, true);
        heart
    }

    fn reset(&mut self, width: f32, height: f32, anywhere: bool) {
        self.x = rand::gen_range(0.0, width);
        self.y = if anywhere {
            rand::gen_range(0.0, height)
        } else {
            rand::gen_range(height + 10.0, height + 80.0)
        };
        self.size = rand::gen_range(10.0, 24.0);
        self.speed = rand::gen_range(18.0, 42.0);
        self.drift = rand::gen_range(-18.0, 18.0);
        self.phase = rand::gen_range(0.0, std::f32::consts::TAU);
        self.color = if rand::gen_range(0, 3) == 0 {
            Color::new(1.0, 0.25, 0.45, 1.0)
        } else {
            Color::new(1.0, rand::gen_range(0.05, 0.35), 0.25, 1.0)
        };
    }

    fn update(&mut self, width: f32, height: f32) {
        let dt = get_frame_time();
        self.phase += dt * 2.0;
        self.y -= self.speed * dt;
        self.x += (self.drift + self.phase.sin() * 12.0) * dt;

        if self.y < -self.size * 2.0 {
            self.reset(width, height, false);
        }

        if self.x < -self.size * 2.0 {
            self.x = width + self.size * 2.0;
        } else if self.x > width + self.size * 2.0 {
            self.x = -self.size * 2.0;
        }
    }

    fn draw(&self) {
        let pulse = 1.0 + self.phase.sin() * 0.08;
        let size = self.size * pulse;
        let alpha = 0.7 + self.phase.sin() * 0.2;
        let color = Color::new(self.color.r, self.color.g, self.color.b, alpha);
        let lobe_offset = size * 0.42;

        draw_circle(self.x - lobe_offset, self.y - lobe_offset * 0.35, size * 0.45, color);
        draw_circle(self.x + lobe_offset, self.y - lobe_offset * 0.35, size * 0.45, color);
        draw_triangle(
            Vec2::new(self.x - size * 0.82, self.y - size * 0.05),
            Vec2::new(self.x + size * 0.82, self.y - size * 0.05),
            Vec2::new(self.x, self.y + size * 0.95),
            color,
        );
        draw_circle(
            self.x - size * 0.2,
            self.y - size * 0.45,
            size * 0.12,
            Color::new(1.0, 0.85, 0.9, alpha * 0.8),
        );
    }
}

struct Drop {
    x: f32,
    y: f32,
    length: f32,
    speed: f32,
}

impl Drop {
    fn new(width: f32, height: f32) -> Self {
        let mut drop = Self {
            x: 0.0,
            y: 0.0,
            length: 0.0,
            speed: 0.0,
        };
        drop.reset(width, height, true);
        drop
    }

    fn reset(&mut self, width: f32, height: f32, anywhere: bool) {
        self.x = rand::gen_range(0.0, width);
        self.y = if anywhere {
            rand::gen_range(-height, height)
        } else {
            rand::gen_range(-height * 0.25, -10.0)
        };
        self.length = rand::gen_range(12.0, 28.0);
        self.speed = rand::gen_range(260.0, 450.0);
    }

    fn update(&mut self, width: f32, height: f32) {
        let dt = get_frame_time();
        self.y += self.speed * dt;

        if self.y > height + self.length {
            self.reset(width, height, false);
        }
    }

    fn draw(&self) {
        draw_line(
            self.x,
            self.y,
            self.x + 2.0,
            self.y + self.length,
            1.4,
            Color::new(0.55, 0.78, 1.0, 0.5),
        );
    }
}

#[macroquad::main("Hearts and Rain")]
async fn main() {
    let mut hearts = Vec::new();
    let mut drops = Vec::new();

    for _ in 0..55 {
        hearts.push(Heart::new(screen_width(), screen_height()));
    }
    for _ in 0..140 {
        drops.push(Drop::new(screen_width(), screen_height()));
    }

    loop {
        let width = screen_width();
        let height = screen_height();

        clear_background(Color::new(0.04, 0.02, 0.08, 1.0));

        for drop in &mut drops {
            drop.update(width, height);
            drop.draw();
        }

        for heart in &mut hearts {
            heart.update(width, height);
            heart.draw();
        }

        next_frame().await;
    }
}
